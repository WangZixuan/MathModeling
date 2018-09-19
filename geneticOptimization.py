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
# from multiprocessing import Pro

loopTime = 10000
populationSize = 500
crossPercent = 0.01
mutaPercent = 0.02
curOptimalSolution = 0
curOptimalScore = 0 
numofMutedGenes = 50

def repairOperator(singleSolution,pucks,gates):
    return repair.repair(singleSolution,pucks,gates)

def evaluateOperator(population,pucks,gates):
    if check_feasibility(population, pucks, gates):
        if np.random.ranf() <= 0.5:
            population = repair.repair(population,pucks,gates)
        return [population,population.sum() - 0.5*np.sign(np.sum(population, axis=0)).sum()]
    else:
        if np.random.ranf() <= 0.5:
            try:
                population = repair.repair(population,pucks,gates)
                return [population,population.sum() - 0.5*np.sign(np.sum(population, axis=0)).sum()]
            except Exception:
                print('Evaluator Error')
                # np.savetxt('wa.txt',population,fmt='%d',delimiter=',')
                exit(-1)
        else:
            return [population,1]

def selectOperator(pop2ScoreSet):
    try:
        tmp = [s for s in pop2ScoreSet] 
        pop2ScoreSet = []
        sorted(tmp,key=lambda k:k[1])
    except:
        print('Sort Error',[k[1] for k in tmp])
        exit(-1)

    #add the top 2 opt solution to save directly
    for i in range(1):
        pop2ScoreSet.append(tmp[min(i,len(tmp)-1)])

    # remove the first two from tmp list 
    try:
        totalScore = reduce(lambda x,y:x+y[1], tmp, 0)
    except:
        print(totalScore)
    weighted_probability = np.array([s[1] / totalScore for s in tmp])
    weighted_probability /= weighted_probability.sum()
    
    for item in random.choice(range(len(tmp)), populationSize-2, p = weighted_probability):
        pop2ScoreSet.append(copy.deepcopy(tmp[item]))
    return pop2ScoreSet

def crossoverOperator(pop2ScoreSet):
    # oldPolulation = [s for s in pop2ScoreSet]
    # print('CrossOver Running')
    Index = list(range(len(pop2ScoreSet)))
    numofGenes = pop2ScoreSet[0][0].shape[0]
    crossTimes = int(crossPercent*len(pop2ScoreSet))

    for index in range(crossTimes):
        [index1,index2] = random.choice(Index,2,replace=False)
        try:
            Index.remove(index1)
            Index.remove(index2)
        except:
            print('Cross Error')
            exit(-1)
        crossoverIndex = random.randint(0,numofGenes)
        a = pop2ScoreSet[index1][0][crossoverIndex][:]
        b = pop2ScoreSet[index2][0][crossoverIndex][:]
        pop2ScoreSet[index1][0][crossoverIndex][:] = b 
        pop2ScoreSet[index2][0][crossoverIndex][:] = a
    # for item in oldPolulation:
        # pop2ScoreSet.append(item)
    return pop2ScoreSet
    
def mutationOperator(pop2ScoreSet,pucks,gates):
    Index = list(range(len(pop2ScoreSet)))
    numofGenes = pop2ScoreSet[0][0].shape[0]
    numofGenesDim = pop2ScoreSet[0][0].shape[1]
    mutaTimes = int(mutaPercent*len(pop2ScoreSet))
    
    for index in range(random.randint(0,mutaTimes)):
    #每轮随机挑选 mutaTimes个解进行变异 
        [index1] = random.choice(Index,1)
        # Index.remove(index1)
        for loop in range(random.randint(0,numofMutedGenes)):
            #每次变异 numofMutedGenes 个基因    
            try:
                mutaIndex = random.randint(0,numofGenes-1)
                pop2ScoreSet[index1][0][mutaIndex] =  np.zeros(numofGenesDim)
                mutaSwitch = np.random.ranf()
                if mutaSwitch < 0.5:
                    changeIndex = random.choice(pucks[mutaIndex].available_gates,1)
                    pop2ScoreSet[index1][0][mutaIndex][changeIndex] = 1
            except Exception as ex:
                print('Muta Error')
                exit(-1)
    return pop2ScoreSet
        
def geneticOptimization(populationSet,pucks,gates,id):
    global curOptimalSolution
    global curOptimalScore 
    pop2ScoreSet = [[s,0] for s in populationSet]
    loopIndex = 0
    while(True):
        loopIndex += 1
        for index in range(len(pop2ScoreSet)):
            pop2ScoreSet[index] = evaluateOperator(pop2ScoreSet[index][0],pucks,gates)

        scores  = [s[1] for s in pop2ScoreSet]
        localOptimalScore = max(scores)
        print(loopIndex,'round','optimal score',curOptimalScore,len(pop2ScoreSet),[s[1] for s in pop2ScoreSet])
        # print('1',len(pop2ScoreSet))
        # 
        pop2ScoreSet = selectOperator(pop2ScoreSet)

        if(localOptimalScore > curOptimalScore):
            for item in pop2ScoreSet:
                if item[1] >= localOptimalScore:
                    curOptimalScore = item[1]
                    curOptimalSolution = item[0]
                    np.savetxt('opt'+str(id)+'.txt',curOptimalSolution,fmt='%d',delimiter=',')
        pop2ScoreSet.append([curOptimalSolution,curOptimalScore])
        # print('3',[s[1] for s in pop2ScoreSet])
        pop2ScoreSet = crossoverOperator(pop2ScoreSet)
        # print('3',[s[1] for s in pop2ScoreSet])
        pop2ScoreSet = mutationOperator(pop2ScoreSet,pucks,gates)
        # print('3',[s[1] for s in pop2ScoreSet])

if __name__ == "__main__":
    populationSet = []
    curOptimalScore = 0
    gates = Gates.Gates().all_gates
    pucks = Pucks.Pucks(gates=gates).all_pucks
    a = np.loadtxt("result-greedy.csv", delimiter=',')
    # populationSet.append(a)
    # a = np.loadtxt("result.csv", delimiter=',')
    populationSet.append(a)
    # pool = mp.Pool()
    # info('main line')
    pset = [ ]
    for process in range(min(mp.cpu_count()-2,100)):
        p = mp.Process(target=geneticOptimization, args=([s for s in populationSet],pucks,gates,process,))
        p.start()
        pset.append(p)
    
    for p in pset:
        p.join()
    # geneticOptimization(populationSet,pucks,gates,1)

from initialize import *

# coding:utf-8
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
from ticketsMatrix import *
from transferTime import *

g = Gates.Gates().all_gates
p = Pucks.Pucks(gates=g).all_pucks
t = Tickets.Tickets().all_tickets
matrix = get_path_matrix(p, t)


# print(matrix.sum())

def score(allocation, pucks, gates):
    F = np.zeros([303, 303])
    for i in range(303):
        if (allocation[i, :].sum() == 0):
            continue
        index1 = pucks[i].arrive_type
        index2 = gates[list(allocation[i, :]).index(1)].terminal
        for j in range(303):
            if (allocation[j, :].sum() == 0):
                continue
            index3 = pucks[j].depart_type
            index4 = gates[list(allocation[j, :]).index(1)].terminal
            # print(allocation[j,:].sum())
            # print(index1,index2,index3,index4)
            F[i, j] = PaperWorkTime[index1 + index2 + '-' + index3 + index4]
    newMatrix = copy.deepcopy(matrix)
    for i in range(303):
        if allocation[i, :].sum() == 0:
            newMatrix[i, :] = np.zeros(303)
            newMatrix[:, i] = np.zeros(303)
    # print(newMatrix.sum())
    print([allocation.sum(), (F * matrix).sum(), np.sign(np.sum(allocation, axis=0)).sum(),
           (F * matrix).sum() / newMatrix.sum()])
    return allocation.sum() - (F * matrix).sum() - np.sign(np.sum(allocation, axis=0)).sum(), [allocation.sum(),
                                                                                               (F * matrix).sum(),
                                                                                               np.sign(
                                                                                                   np.sum(allocation,
                                                                                                          axis=0)).sum(),
                                                                                               (
                                                                                                           F * matrix).sum() / newMatrix.sum()]


def transpose_1(a, pucks, gates):
    # unorder_set = list(range(303))
    s = copy.deepcopy(a)
    unassign = []
    assigned = []
    for index in range(s.shape[0]):
        if s[index, :].sum() == 0:
            unassign.append(index)
        else:
            assigned.append(index)
    # gateSet = random.choice(list(range(69)),random.randint(1,3),replace=False)
    gateSet = range(10, 19)
    for gate in gateSet:
        for index in range(303):
            if s[index, gate] == 1:
                unassign.append(index)
                assigned.remove(index)
    for gate in gateSet:
        s[:, gate] = np.zeros(303)
    newPucks = [pucks[k] for k in unassign]
    newPucks.sort(key=compare_func.cmp_to_key(puck_compare_depart_and_stay_time))
    for item in newPucks:
        for index in range(68, 0, -1):
            if (can_add(s, pucks, gates, item.id, index)):
                add_puck(s, pucks, gates, item.id, index)
    return s


def transpose_2(a, pucks, gates):
    for loop in range(100):
        index1 = random.randint(0, 69)
        index2 = random.randint(0, 69)
        if (index1 == index2):
            continue
        if (gates[index1].flight_type != gates[index2].flight_type):
            continue
        if (gates[index1].arrive_type_D != gates[index2].arrive_type_D):
            continue
        if (gates[index1].arrive_type_D != gates[index2].arrive_type_D):
            continue
        if (gates[index1].depart_type_D != gates[index2].depart_type_D):
            continue
        if (gates[index1].depart_type_I != gates[index2].depart_type_I):
            continue
        tmp = copy.deepcopy(a[:, index1])
        a[:, index1] = copy.deepcopy(a[:, index2])
        a[:, index2] = copy.deepcopy(tmp)
        return a
    return a


def transpose_3(a, pucks, gates):
    for loop in range(100):
        index1 = random.randint(0, 69)
        index2 = random.randint(0, 69)
        if (index1 == index2):
            continue
        if (gates[index1].flight_type != gates[index2].flight_type):
            continue
        if (gates[index1].arrive_type_D != gates[index2].arrive_type_D):
            continue
        if (gates[index1].depart_type_I != gates[index2].depart_type_I):
            continue
        tmp = copy.deepcopy(a[:, index1])
        a[:, index1] = copy.deepcopy(a[:, index2])
        a[:, index2] = copy.deepcopy(tmp)
        return a
    return a


def move(allocation, pucks, gates):
    print(score(allocation, pucks, gates))
    assign = []
    for line in range(allocation.shape[0]):
        if (allocation[line, :].sum() > 0):
            assign.append(line)

    for item in assign:
        for index in range(68, 0, -1):
            allocation, dindex = delete_puck(allocation, item)
            # add_puck(allocation, pucks, gates, item, dindex)
            allocation, re = add_puck(allocation, pucks, gates, item, index)
            if (not re):
                add_puck(allocation, pucks, gates, item, dindex)
            # if(can_add(allocation,pucks,gates,item,index)):
    np.savetxt('opt' + '.txt', allocation, fmt='%d', delimiter=',')
    print(score(allocation, pucks, gates))


def transpose_3(a, pucks, gates):
    pass


def safunc(a, pucks, gates):
    curScore, w = score(a, pucks, gates)
    optScore, w = score(a, pucks, gates)
    optSec = w[1]
    optThi = w[1]
    maxK = 100
    T = 1000
    Tmin = 10
    k = 100
    t = 0
    while T >= Tmin:
        for k in range(maxK):
            # print('gg',curScore,optScore)
            # newAllocation = transpose_1(a,pucks,gates)
            newAllocation = transpose_2(a, pucks, gates)
            newScore, b = score(newAllocation, pucks, gates)
            if not check_feasibility(newAllocation, pucks, gates):
                exit(-1)
            print(optScore, newAllocation.sum(), np.sign(np.sum(newAllocation, axis=0)).sum())
            if newScore > curScore:
                a = copy.deepcopy(newAllocation)
                curScore = newScore
                if newScore > optScore or (b[1] < optSec):
                    optScore = newScore
                    optSec = b[1]
                    np.savetxt('opt2' + '.txt', a, fmt='%d', delimiter=',')
                    # exit(-1)
            else:
                p = math.exp(-(newScore - optScore) / T)
                r = np.random.uniform(low=0, high=1)
                if r < p:
                    a = copy.deepcopy(newAllocation)
                    curScore = newScore
        t += 1
        T = 1000 / math.log2(1 + t)


if __name__ == '__main__':
    g = Gates.Gates().all_gates
    p = Pucks.Pucks(gates=g).all_pucks
    a = np.loadtxt("opt.csv", delimiter=',')
    # transpose_1(a, p, g)
    # np.savetxt('opt'+'.txt',a,fmt='%d',delimiter=',')

    # move(a,p,g)
    #
    safunc(a, p, g)

    # print(can_add(a, p, g, 0, 0))

#
#



