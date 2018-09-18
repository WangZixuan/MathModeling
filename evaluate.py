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

def evaluateOperator(population,pucks,gates):
    if check_feasibility(population, pucks, gates):
        return population.sum() - 0.5*np.sign(np.sum(population, axis=0)).sum()
    else:
        return 0

if __name__=="__main__":
    gates = Gates.Gates().all_gates
    pucks = Pucks.Pucks(gates=gates).all_pucks
    for id in range(mp.cpu_count()-2):
        try:
            population = np.loadtxt('opt'+'.txt', delimiter=',')
            print(evaluateOperator(population,pucks,gates))
        except:
            print('File load error')
            exit(-1)
        