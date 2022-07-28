# iDistance

A written from scratch Python implementation of iDistance: An Adaptive B+-tree Based Indexing Method for Nearest Neighbor Search.

Added some fitting methods.

The project is not completed and is under development.

bPlusTree.py modified from https://gist.github.com/benben233/2c8a2a8ab44a7beabad0df1b6658232e

### Papers cite and abstract

Jagadish, H & Jagadish, V & Ooi, Beng & Tan, K.-L & Zhang, Rui & bullet,. (2005). iDistance: An Adaptive B+-tree Based Indexing Method for Nearest Neighbor Search. ACM Transactions on Database Systems. 30. 364-397. In this article, we present an efficient B + -tree based indexing method, called iDistance, for K-nearest neighbor (KNN) search in a high-dimensional metric space. iDistance partitions the data based on a space-or data-partitioning strategy, and selects a reference point for each parti-tion. The data points in each partition are transformed into a single dimensional value based on their similarity with respect to the reference point. This allows the points to be indexed using a B + -tree structure and KNN search to be performed using one-dimensional range search. The choice of partition and reference points adapts the index structure to the data distribution. We conducted extensive experiments to evaluate the iDistance technique, and report results demonstrating its effectiveness. We also present a cost model for iDistance KNN search, which can be exploited in query optimization.

https://www.comp.nus.edu.sg/~ooibc/papers/techreport_final.pdf
