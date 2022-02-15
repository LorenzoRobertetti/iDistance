import numpy as np
import bisect

class answerSet():
    
    def __init__(self, q):
        
        self.len = 0
        self.answerSet = []
        self.sortedDist = []
        self.furthestDist = 0
        self.q = q
        
        
    def addPoint(self, dist, value):
        
        index = bisect.bisect_left(self.sortedDist, dist)
        
        self.sortedDist.insert(index, dist) 
        self.answerSet.insert(index, value)
        
        self.len += 1
        
        self.furthestDist = self.sortedDist[self.len - 1]
        
        
    
    def deleteFurthest(self):
        
        self.sortedDist.pop()
        self.answerSet.pop()
        
        self.len -= 1


        
        
        