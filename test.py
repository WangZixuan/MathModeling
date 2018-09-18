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
import matplotlib.pyplot as plt


gates = Gates.Gates().all_gates
pucks = Pucks.Pucks(gates=gates).all_pucks
a = np.loadtxt("result-greedy.csv", delimiter=',')
# print(a[:,0].shape)
cnt = 0 
for index in range(303):
    # print(a[:][1])
    if a[index,:].sum() > 0:
        cnt+=1
print(cnt)
        

for index in range(69):
    # print(a[:][1])
    if a[:,index].sum() == 0:
        print(index+1)


list1 = [] 
for plane in range(303):
    try:
        placedGate = list(a[plane][:]).index(1)
    except:
        placedGate = -1

    if placedGate < 0:
        list1.append(plane)
print(list1)
        
        