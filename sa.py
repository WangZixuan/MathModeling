#coding:utf-8
from helper import *
import numpy as np
from numpy import random
from functools import reduce
import Pucks
import Gates
import compare_func
from checkFeasibility import *
import repair
import multiprocessing as mp
import os
import time
import copy
import math

# def can_add(allocation, pucks, gates, index_puck, index_gate):


# def add_puck(allocation, pucks, gates, index_puck, index_gate):


# def delete_puck(allocation, index_puck):




def score(allocation):
    return allocation.sum() - 0.5*np.sign(np.sum(allocation, axis=0)).sum()
    
def transpose(a, pucks, gates):
    # unorder_set = list(range(303))
    s = copy.deepcopy(a)
    unassign = []
    assigned = []
    for index in range(s.shape[0]):
        if s[index,:].sum()==0:
            unassign.append(index)
        else:
            assigned.append(index)
    cIndex = random.choice(assigned)
    delete_puck(s, cIndex)
    for item in unassign:
        for index in range(69):
            if(can_add(s,pucks,gates,item,index)):
                add_puck(s, pucks, gates, cIndex, index)
    return s

def safunc(a,pucks,gates):
    curScore = score(a)
    optScore = score(a)
    maxK = 100
    T=1000 
    Tmin=10 
    k=100
    t=0
    while T >= Tmin:
        for k in range(maxK):
            print(curScore)
            newAllocation = transpose(a,pucks,gates)
            newScore = score(newAllocation)
            if newScore > curScore:
                a = copy.deepcopy(newAllocation)
                curScore = newScore 
                if newScore > optScore:
                    optScore = newScore
                    np.savetxt('opt'+'.txt',a,fmt='%d',delimiter=',')
            else:
                p = math.exp(-(newScore-optScore)/T)
                r = np.random.uniform(low=0,high=1)
                if r < p:                     
                    a = copy.deepcopy(newAllocation)
                    curScore = newScore
        t+=1
        T=1000/math.log2(1+t)

if __name__ == '__main__':
    g = Gates.Gates().all_gates
    p = Pucks.Pucks(gates=g).all_pucks
    a = np.loadtxt("result-greedy.csv", delimiter=',')
    safunc(a,p,g)
    # print(can_add(a, p, g, 0, 0))