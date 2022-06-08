import numpy as np
from answerSet import answerSet
from fitter import *
from bPlusTree import BPlusTree


class iDistanceNN():
    
    def __init__(self, n_neighbors):
        
        self.k = n_neighbors

# ###################### I DISTANCE ##############################

    def kNeighbors(self, q):
        
        self.radius = 0
        self.stopFlag = False
        self.s = answerSet(q)
        self.q = q
        
        self.lp, self.rp, self.oflag, self.oDist, self.isLeftStarted, self.isRightStarted = self.initialize()

        while(self.stopFlag == False):
            if(self.radius > self.c):
                print("break for maxRadius")
                break
            self.radius += self.dRadius
            self.searchO(self.q, self.radius)
    
        return self.s
    
    def searchO(self, q, radius):

        furthestPointDist = self.s.furthestDist
        
        if (furthestPointDist < self.radius and (self.s.len == self.k)):
            self.stopFlag = True

        
        for i in range(self.m):
            
            if (not self.oflag[i]):
                
                if (self.sphereContains(self.q, i)):
                    
                    self.oflag[i] = True
                    
                    lnode = self.bplustree.find(i * self.c + self.oDist[i])
                    
                    self.lp[i] = self.searchInward(lnode, i * self.c + self.oDist[i] - self.radius, i, True)
                    self.rp[i] = self.searchOutward(lnode, i * self.c + self.oDist[i] + self.radius, i, True)
                    
                else:
                    if (self.intersectsSpheres(self.q, i, self.radius)):
                        self.oflag[i] = True

                        lnode = self.bplustree.find(i * self.c + self.o[i].max_r)
                        self.lp[i] = self.searchInward(lnode, i * self.c + self.oDist[i] - self.radius, i, False)
            
            else:
                if (not(self.lp[i] == None)):
                    self.lp[i] = self.searchInward(self.lp[i].prev, i * self.c + self.oDist[i] - self.radius, i, False)
                if (not(self.rp[i] == None)):
                    self.rp[i] = self.searchOutward(self.rp[i].next, i * self.c + self.oDist[i] + self.radius, i, False)
        
        return
    
    
    def searchInward(self, node, ivalue, partition, check):
        
        if(node == None): return None
        
        for j in range(1, len(node.keys) + 1):
                
            valuesList = node.values[len(node.keys) - j]

            if(valuesList[0][1] != partition):
                 if(self.isLeftStarted[partition]):
                    return None
            else:
                if(not(self.isLeftStarted[partition])):
                    self.isLeftStarted[partition] = True
                
                for value in valuesList:

                    furthestPointDist = self.s.furthestDist
                    curr_dist = np.linalg.norm(value[2] - self.q)

                    if (self.s.len == self.k):

                        if (curr_dist < furthestPointDist):

                            self.s.deleteFurthest()
                            self.s.addPoint(curr_dist, value)

                    else:
                        self.s.addPoint(curr_dist, value)

                
        if(node.keys[0] > ivalue):
            node = self.searchInward(node.prev, partition * self.c + self.oDist[partition] - self.radius, partition, False)
        
        return node
    
    def searchOutward(self, node, ivalue, partition, check):
        
        if(node == None): return None
    
        if(not(check)):
    
            for j in range(len(node.keys)):
                        
                valuesList = node.values[j]
                
                if(valuesList[0][1] != partition):
                    if(self.isRightStarted[partition]):
                        return None
                else:

                    if(not(self.isRightStarted[partition])):
                            self.isRightStarted[partition] = True

                    for value in valuesList:

                        furthestPointDist = self.s.furthestDist
                        curr_dist = np.linalg.norm(value[2] - self.q)

                        if (self.s.len == self.k):

                            if (curr_dist < furthestPointDist):

                                self.s.deleteFurthest()
                                self.s.addPoint(curr_dist, value)

                        else:
                            self.s.addPoint(curr_dist, value)

        if(node.keys[len(node.keys) - 1] < ivalue):
            node = self.searchOutward(node.next, partition * self.c + self.oDist[partition] + self.radius, partition, False)
        
        return node
                
    def sphereContains(self, q, partition):
        return True if (self.oDist[partition] < self.o[partition].max_r) else False
          
    
    def intersectsSpheres(self, q, partition, radius):
        return True if (self.oDist[partition] < (self.o[partition].max_r + self.radius)) else False

# #################### INIT FUNCTION #########################

    def initialize(self):
        
        lp = [None for i in range(self.m)]
        rp = [None for i in range(self.m)]
        oflag = [False for i in range(self.m)]
        isLeftStarted = [False for i in range(self.m)]
        isRightStarted = [False for i in range(self.m)]
        oDist = [np.linalg.norm(self.o[i].vect - self.q) for i in range(self.m)]

        return lp, rp, oflag, oDist, isLeftStarted, isRightStarted

# #################### FIT ############################################


    def fit(self, n_cluster, dataSpace):
        
        self.o, self.c, self.dRadius, self.mapO = clusterFit(n_cluster, dataSpace)
        self.m = len(self.o)
        self.bplustree = BPlusTree()
        self.treeFill(dataSpace, self.bplustree, self.o, self.mapO, self.c)




# ##################### TREE OPERATIONs #################################

    def treeFill(self, dataSpace, bplustree, o, mapO, c):
        
        
        count = 0
        
        for i in range(len(dataSpace)):
            
            curr_dist = np.linalg.norm(dataSpace[i] - o[mapO[i]].vect)
            key = mapO[i] * c + curr_dist

            value = [(i, mapO[i], dataSpace[i])]

            ins, leaf = bplustree.insert(key, value)
            
            if(not(ins)):
                for j in range(len(leaf.keys)):
                    if key == leaf.keys[j]:
                        leaf.values[j] += value
                        count += 1
                        
        print(self.treeElem(), '            ', count)
    
    def insertOne(self, pointToInsert):
        
        minValue = float("+inf")
        flag = -1
        
        for i in range(self.m):
            curr_dist = np.linalg.norm(pointToInsert - self.o[i].vect)
            if(curr_dist < minValue):
                minValue = curr_dist
                flag = i

        key = flag * self.c + minValue

        value = [(99, flag, pointToInsert)]

        ins, _ = self.bplustree.insert(key, value)
        
        return ins
    
    def deleteOne(self, pointToDelete): #aggiungere id
        
        minValue = float("+inf")
        flag = -1
        
        for i in range(self.m):
            curr_dist = np.linalg.norm(pointToDelete - self.o[i].vect)
            if(curr_dist < minValue):
                minValue = curr_dist
                flag = i

        key = flag * self.c + minValue
        
        delete = self.bplustree.delete(key) #devo modificare la struttura per poter eliminare chiave + id 
        
        return delete
    
    def treeElem(self):
        leaf = self.bplustree.find(0)
        count = 0
        while (leaf != None):
            count += len(leaf.keys)
            leaf = leaf.next
        return count

# ##########################################################################
