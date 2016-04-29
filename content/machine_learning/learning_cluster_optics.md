Title: Clustering based on density
Date: 2016-01-08
Category: Algorithm
Tag: Cluster, Optics, DBSCAN, Dcluster

## 1. Background

&nbsp;&nbsp; Clustering is widely used in data mining tasks. There are too much clustering methods to learn all of them. Here we are trying to learn from the very beginning.

&nbsp;&nbsp; If we have mounts of data collected, it is a wise way to find clusters from them. Density based methods are remarkable in this kind of work.



## 2. Distance measurement

(To do)

### 2.2 SSE measurement

![Pic](/theme/images/1.gif)

```$ SSE = \sum_{i=1}^{K}\sum_{x\in C_x}(c_i-x)^2 $```

## 3. DBSCAN

### 3.1 Definations.
- Eps: Threshold of distance for measuring density.
- Minpt: Minimum number of points to define a core point.
- Core points: Points with the count of points within distance of Eps greater than Minpt.
- Border points: Points fall into the neighbor of core points.
- Noise points: Points left.

### 3.2 Procedure
- Label all points.
- Eliminate noise points.
- Connect core points within distance Eps.
- Regard each core points group as a cluster and collect bordor points from core.

### 3.3 Time and space complexity
- Time: O(m^2). Might be reduced to O(m*logM) if kd-trees are used for find nearest k neighbors with low dimensions.
- Space: O(m). Only need to store whether it is a core point or border point or noise.

> [kd-trees](http://www.cnblogs.com/slysky/archive/2011/11/08/2241247.html)

### 3.4 Selection of parameters.




## 2. Related links:
- [Free mind's blog - talking about clustering](http://blog.pluskid.org/?page_id=78)





## Optics
### Related links:
- [ryangomba/optics.py](https://gist.github.com/ryangomba/1724881) : A python module for optics, 2-dim supported only.
- [Michal Daszykowski](http://chemometria.us.edu.pl/download/optics.py) :



## Pycluster
- [Home](https://github.com/annoviko/pyclustering)
- [Docs](https://github.com/annoviko/pyclustering/blob/0.5/docs/apidoc-pyclustering-0.5.pdf)



