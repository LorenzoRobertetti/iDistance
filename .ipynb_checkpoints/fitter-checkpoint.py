import numpy as np
from Oi import O
from sklearn.cluster import KMeans

def hyperCubeStats(dim, dataSpace): #voglio ritornare il vettore di spostamento e la lunghezza del lato
    
    #calcolo la costante c e il delta dell'incremento
    #c la prendo due volte la diagonale dell'iper-cubo
    #il delta lo prendo come 1% del lato dell'iper-cubo
    
    l = 0
    
    #calcolo la lunghezza del lato
    for i in range(dim):
        minValue = float("+inf")
        maxValue = float("-inf")
        for j in range(len(dataSpace)):
            if (dataSpace[j][i] > maxValue):
                maxValue = dataSpace[j][i]
            if (dataSpace[j][i] < minValue):
                minValue = dataSpace[j][i]
        
        curr_l = abs(maxValue - minValue)
        
        if(curr_l > l):
            l = curr_l
    
    #calcolo la lunghezza della diagonale
    orig = np.zeros(dim)
    edge = np.zeros(dim)
    for i in range(len(edge)):
        edge[i] = l
    
    diag = np.linalg.norm(edge - orig) #da fare con radice 
    
    c = 2 * diag #due volte la diagonale
    dRadius = l/100 #1%
    
    #calcolo i punti di riferimento pensando il cubo centrato nell'orgine
    o = []
    i = 0
    j = 0 
    while(i < dim):
        
        O1 = O(np.zeros(dim))
        O2 = O(np.zeros(dim))
        
        O1.vect[i] = l/2
        O2.vect[i] = -l/2
        
        o.append(O1)
        o.append(O2)
        i += 1

    #calcolo il centro del cluster
    kmeans = KMeans(n_clusters = 1, random_state = 0).fit(dataSpace)
    
    s = kmeans.cluster_centers_[0]
    
    #traslo i vettori di riferimento rispetto al centro del cluster
    for i in range(len(o)):
        o[i].vect += s
        
    #calcolo la mappa dei vettori
    mapO = np.zeros(len(dataSpace), dtype = int)
    
    for i in range(len(dataSpace)):
        
        minValue = float('+inf')

        for j in range(len(o)):
            curr_dist = np.linalg.norm(dataSpace[i] - o[j].vect)
            if (curr_dist < minValue):
                minValue = curr_dist
                mapO[i] = j
            
    #calcolo il max_r di ogni vettore di riferimento
    for j in range(len(o)):
        maxValue = float("-inf")

        for i in range(len(dataSpace)):
            if(mapO[i] == j):
                curr_dist = np.linalg.norm(dataSpace[i] - o[j].vect)
                if curr_dist > o[j].max_r :
                    maxValue = curr_dist
                    o[j].max_r = curr_dist
    
    
    return o, c, dRadius, mapO

def hyperCubeFurthestFit(dim, dataSpace): #voglio ritornare il vettore di spostamento e la lunghezza del lato
    
    #calcolo la costante c e il delta dell'incremento
    #c la prendo due volte la diagonale dell'iper-cubo
    #il delta lo prendo come 1% del lato dell'iper-cubo
    
    l = 0
    
    #calcolo la lunghezza del lato
    for i in range(dim):
        minValue = float("+inf")
        maxValue = float("-inf")
        for j in range(len(dataSpace)):
            if (dataSpace[j][i] > maxValue):
                maxValue = dataSpace[j][i]
            if (dataSpace[j][i] < minValue):
                minValue = dataSpace[j][i]
        
        curr_l = abs(maxValue - minValue)
        
        if(curr_l > l):
            l = curr_l
    
    #calcolo la lunghezza della diagonale
    orig = np.zeros(dim)
    edge = np.zeros(dim)
    for i in range(len(edge)):
        edge[i] = l
    
    diag = np.linalg.norm(edge - orig) #da fare con radice 
    
    c = 2 * diag #due volte la diagonale
    dRadius = l/100 #1%
    
    #calcolo i punti di riferimento pensando il cubo centrato nell'orgine
    o = []
    i = 0
    j = 0 
    while(i < dim):
        
        O1 = O(np.zeros(dim))
        O2 = O(np.zeros(dim))
        
        O1.vect[i] = l/2
        O2.vect[i] = -l/2
        
        o.append(O1)
        o.append(O2)
        i += 1

    #calcolo il centro del cluster
    kmeans = KMeans(n_clusters = 1, random_state = 0).fit(dataSpace)
    
    s = kmeans.cluster_centers_[0]
    
    #traslo i vettori di riferimento rispetto al centro del cluster
    for i in range(len(o)):
        o[i].vect += s
        
    #calcolo la mappa dei vettori
    mapO = np.zeros(len(dataSpace), dtype = int)
    
    for i in range(len(dataSpace)):
        
        maxValue = float('-inf')

        for j in range(len(o)):
            curr_dist = np.linalg.norm(dataSpace[i] - o[j].vect)
            if (curr_dist > maxValue):
                maxValue = curr_dist
                mapO[i] = j
            
    #calcolo il max_r di ogni vettore di riferimento
    for j in range(len(o)):
        maxValue = float("-inf")

        for i in range(len(dataSpace)):
            if(mapO[i] == j):
                curr_dist = np.linalg.norm(dataSpace[i] - o[j].vect)
                if curr_dist > o[j].max_r :
                    maxValue = curr_dist
                    o[j].max_r = curr_dist
    
    
    return o, c, dRadius, mapO
    
def fit(dataSpace):
    
    dim = len(dataSpace[0]) #prendo il numero di dimensioni dal primo elemento, da cambiare
    
    o, c, dRadius, mapO = hyperCubeStats(dim, dataSpace)
    
    return o, c, dRadius, mapO

def clusterFit(num_cluster, dataSpace):
    
    dim = len(dataSpace[0])
    
    l = 0
    
    #calcolo la lunghezza del lato
    for i in range(dim):
        minValue = float("+inf")
        maxValue = float("-inf")
        for j in range(len(dataSpace)):
            if (dataSpace[j][i] > maxValue):
                maxValue = dataSpace[j][i]
            if (dataSpace[j][i] < minValue):
                minValue = dataSpace[j][i]
        
        curr_l = abs(maxValue - minValue)
        
        if(curr_l > l):
            l = curr_l
    
    #calcolo la lunghezza della diagonale
    orig = np.zeros(dim)
    edge = np.zeros(dim)
    for i in range(len(edge)):
        edge[i] = l
    
    diag = np.linalg.norm(edge - orig) #da fare con radice 
    
    c = 2 * diag #due volte la diagonale
    dRadius = l/100 #1%
    
    #calcolo il centro del cluster
    kmeans = KMeans(n_clusters = num_cluster, random_state = 0).fit(dataSpace)
    
    clusterCenters = kmeans.cluster_centers_
    
    o = []
    
    for i in range(len(clusterCenters)):
        Oi = O(clusterCenters[i])
        o.append(Oi)
        
    #calcolo la mappa dei vettori
    mapO = np.zeros(len(dataSpace), dtype = int)
    
    for i in range(len(dataSpace)):
        
        minValue = float('+inf')

        for j in range(len(o)):
            curr_dist = np.linalg.norm(dataSpace[i] - o[j].vect)
            if (curr_dist < minValue):
                minValue = curr_dist
                mapO[i] = j
            
    #calcolo il max_r di ogni vettore di riferimento
    for j in range(len(o)):
        maxValue = float("-inf")

        for i in range(len(dataSpace)):
            if(mapO[i] == j):
                curr_dist = np.linalg.norm(dataSpace[i] - o[j].vect)
                if curr_dist > o[j].max_r :
                    maxValue = curr_dist
                    o[j].max_r = curr_dist
    
    return o, c, dRadius, mapO