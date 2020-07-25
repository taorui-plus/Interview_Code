#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Author: TaoRui
Date: 2020/07/10 14:36:33
Description: DBSCAN(Density-Based Spatial Clustering of Application with Noise)是一种典型的基于密度的聚类算法，
在DBSCAN算法中将数据点分为一下三类：
    核心点：在半径Eps内含有超过MinPts数目的点
    边界点：在半径Eps内点的数量小于MinPts，但是落在核心点的邻域内
    噪音点：既不是核心点也不是边界点的点
在这里有两个量，一个是半径Eps，另一个是指定的数目MinPts
"""
import numpy as np
import random


def dist(t1, t2):
    """计算两个点之间的欧式距离
    Args:
        t1: 参数1, tuple
        t2: 参数2, tuple
    """
    dis = np.sqrt((np.power((t1[0] - t2[0]), 2) + np.power((t1[1] - t2[1]), 2)))
    return dis


def dbscan(Data, Eps, MinPts):
    """计算两个点之间的欧式距离
    Args:
        Data: 数据
        Eps: 半径
        MinPts: 最小点数
    """
    num = len(Data)
    unvisited = [i for i in range(num)]
    visited = []
    C = [-1 for i in range(num)]
    # 用k来标记不同的簇，k = -1表示噪声点
    k = -1
    # 如果还有没访问的点
    while len(unvisited) > 0:
        # 随机选择一个unvisited对象
        p = random.choice(unvisited)
        unvisited.remove(p)
        visited.append(p)
        # N为p的epsilon邻域中的对象的集合
        N = []
        for i in range(num):
            if dist(Data[i], Data[p]) <= Eps:
                N.append(i)
        # 如果p的epsilon邻域中的对象数大于指定阈值，说明p是一个核心对象
        if len(N) >= MinPts:
            k = k + 1
            C[p] = k
            # 对于p的epsilon邻域中的每个对象pi
            for pi in N:
                if pi in unvisited:
                    unvisited.remove(pi)
                    visited.append(pi)
                    # 找到pi的邻域中的核心对象，将这些对象放入M中
                    # M是位于pi的邻域中的点的列表
                    M = []
                    for j in range(num):
                        if dist(Data[j], Data[pi]) <= Eps:
                            M.append(j)
                    if len(M) >= MinPts:
                        for t in M:
                            if t not in N:
                                N.append(t)
                # 若pi不属于任何簇，C[pi] == -1说明C中第pi个值没有改动
                if C[pi] == -1:
                    C[pi] = k
        # 如果p的epsilon邻域中的对象数小于指定阈值，说明p是一个噪声点
        else:
            C[p] = -1

    return C


if __name__ == '__main__':
    X = np.array([[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11]])
    eps = 5
    min_Pts = 2
    C = dbscan(X, eps, min_Pts)
    print(C)

