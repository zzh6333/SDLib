from sklearn.metrics.pairwise import pairwise_distances,cosine_similarity
import numpy as np
from numpy.linalg import norm
from scipy.stats.stats import pearsonr
from math import sqrt,exp

def itemmean(set_i):
    # set_i is a dict
    itemmeanlist = {}
    for item in set_i:
        i = set_i[item]
        itemcount = len(i)
        sum = 0
        for user in i:
            sum = i[user] + sum
        avg = sum / itemcount
        itemmeanlist[item] = avg
    return itemmeanlist

def StandardDeviation(set_u):
    # set_u is a dict
    StdDeviation = {}
    for user in set_u:
        d=set_u[user]
        itemnum = len(d)
        sum = 0
        for item in d:
            sum = d[item]+sum
        avg=sum/itemnum
        std=0
        for item in d:
            std = std+(d[item]-avg)*(d[item]-avg)
        std=std/itemnum
        std=np.sqrt(std)
        StdDeviation[user]=std
    return StdDeviation

def DegreeofAgreement(set_u,set_i):
    # set_u and set_i are dicts
    DegAgr = {}
    itemmeanlist = itemmean(set_i)
    for user in set_u:
        d=set_u[user]
        itemnum = len(d)
        sumda = 0
        for item in d:
            sumda = abs(d[item]-itemmeanlist[item])
        sumda = sumda/itemnum
        DegAgr[user]=sumda
    return DegAgr

def DegreeofSimilarity(set_u,K):
    # set_u is a dict , K means top-K
    DegSim = {}
    for user in set_u:
        SimList = []
        DegSim[user] = 0
        for user1 in set_u:
            A = 0
            B = 0
            C = 0
            D = 0
            E = 0
            N = 0
            for item in list(set(set_u[user]).intersection(set(set_u[user1]))):
                A += set_u[user][item]
                B += set_u[user][item]
                N += 1
            if N==0:
                AverageA = 0
                AverageB = 0
            else:
                AverageA = A/N
                AverageB = B/N
            for item in list(set(set_u[user]).intersection(set(set_u[user1]))):
                C += (set_u[user][item]-AverageA)*(set_u[user1][item]-AverageB)
                D += np.square(set_u[user][item]-AverageA)
                E += np.square(set_u[user1][item]-AverageB)
            if C == 0:
                SimList.append(0)
            else:
                SimList.append(C/(np.sqrt(D)*np.sqrt(E)))
        SimList.sort(reverse=True)
        if K <= len(SimList):
            for i in range(1,K):
                DegSim[user] += SimList[i] / K
        else:
            for i in range(1,len(SimList)):
                DegSim[user] += SimList[i] / K
    return DegSim

def RatingDeviation(set_u,set_i):
    # set_u and set_i are dicts
    RDMA = {}
    itemMeans = {}
    for user in set_u:
        Divisor = 0
        for item1 in set_i:
            itemMeans[item1] = sum(set_i[item1].values())/(len(set_i[item1]) + 0)
        for item2 in set_u[user]:
            Divisor += abs(set_u[user][item2]-itemMeans[item2]) / len(set_i[item2])
        RDMA[user]=Divisor / len(set_u[user])
    return RDMA








