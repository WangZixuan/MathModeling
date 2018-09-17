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
# from multiprocessing import Pro

loopTime = 10000
populationSize = 200
crossPercent = 0.015
mutaPercent = 0.015
curOptimalSolution = 0
curOptimalScore = 0 
numofMutedGenes = 5

def repairOperator(singleSolution,pucks,gates):
    return repair.repair(singleSolution,pucks,gates)

def evaluateOperator(population,pucks,gates):
    if check_feasibility(population, pucks, gates):
        return [population,population.sum() - 0.5*np.sign(np.sum(population, axis=0)).sum()]
    else:
        try:
            population = repair.repair(population,pucks,gates)
            return [population,population.sum() - 0.5*np.sign(np.sum(population, axis=0)).sum()]
        except Exception:
            print('Evaluator Error')
            # np.savetxt('wa.txt',population,fmt='%d',delimiter=',')
            exit(-1)

def selectOperator(pop2ScoreSet):
    try:
        tmp = [s for s in pop2ScoreSet] 
        pop2ScoreSet = []
        sorted(tmp,key=lambda k:k[1])
    except:
        print('Sort Error',[k[1] for k in tmp])
        exit(-1)

    #add the top 2 opt solution to save directly
    for i in range(2):
        pop2ScoreSet.append(tmp[min(i,len(tmp)-1)])
    
    # remove the first two from tmp list 
    try:
        totalScore = reduce(lambda x,y:x+y[1], tmp, 0)
    except:
        print(totalScore)
    weighted_probability = np.array([s[1] / totalScore for s in tmp])
    weighted_probability /= weighted_probability.sum()
    
    for item in random.choice(range(len(tmp)), populationSize-2, p = weighted_probability):
        pop2ScoreSet.append(tmp[item])
    return pop2ScoreSet

def crossoverOperator(pop2ScoreSet):
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
    return pop2ScoreSet
    
def mutationOperator(pop2ScoreSet,pucks,gates):
    Index = list(range(len(pop2ScoreSet)))
    numofGenes = pop2ScoreSet[0][0].shape[0]
    numofGenes = pop2ScoreSet[0][0].shape[0]
    numofGenesDim = pop2ScoreSet[0][0].shape[1]
    mutaTimes = int(mutaPercent*len(pop2ScoreSet))

    for index in range(mutaTimes):
    #每轮随机挑选 mutaTimes个解进行变异
        for loop in range(numofMutedGenes):
            #每次变异 numofMutedGenes 个基因
            [index1] = random.choice(Index,1,replace=False)
            try:
                Index.remove(index1)
                mutaIndex = random.randint(0,numofGenes)
                pop2ScoreSet[index1][0][mutaIndex] =  np.zeros(numofGenesDim)
                mutaSwitch = np.random.ranf()
                if mutaSwitch < 0.5:
                    changeIndex = random.choice(pucks[mutaIndex].available_gates,1)
                    pop2ScoreSet[index1][0][mutaIndex][changeIndex] = 1
            except:
                print('Muta Error')
                exit(-1)
    return pop2ScoreSet
        
def geneticOptimization(populationSet,pucks,gates,id):
    global curOptimalSolution
    global curOptimalScore 
    pop2ScoreSet = [[s,0] for s in populationSet]
    for loopIndex in range(loopTime):
        for index in range(len(pop2ScoreSet)):
            pop2ScoreSet[index] = evaluateOperator(pop2ScoreSet[index][0],pucks,gates)
        print(loopIndex,'round','optimal score',curOptimalScore,len(pop2ScoreSet),max([s[1] for s in pop2ScoreSet]))
        # print('1',len(pop2ScoreSet))
        # 
        pop2ScoreSet = selectOperator(pop2ScoreSet)
        # print('2',[s[1] for s in pop2ScoreSet])
        scores  = [s[1] for s in pop2ScoreSet]
        localOptimalScore = max(scores)
        if(localOptimalScore > curOptimalScore):
            for item in pop2ScoreSet:
                if item[1] >= localOptimalScore:
                    curOptimalScore = item[1]
                    curOptimalSolution = item[0]
                    np.savetxt('opt'+str(process)+'.txt',curOptimalSolution,fmt='%d',delimiter=',')
        # print('3',[s[1] for s in pop2ScoreSet])
        pop2ScoreSet = crossoverOperator(pop2ScoreSet)
        # print('3',[s[1] for s in pop2ScoreSet])
        pop2ScoreSet.append([curOptimalSolution,curOptimalScore])
        # print('3',[s[1] for s in pop2ScoreSet])
        pop2ScoreSet = mutationOperator(pop2ScoreSet,pucks,gates)
        # print('3',[s[1] for s in pop2ScoreSet])
        pop2ScoreSet.append([curOptimalSolution,curOptimalScore])
        # print('3',len(pop2ScoreSet))

if __name__ == "__main__":
    populationSet = []
    curOptimalScore = 0
    gates = Gates.Gates().all_gates
    pucks = Pucks.Pucks(gates=gates).all_pucks
    a = np.loadtxt("result-greedy.csv", delimiter=',')
    populationSet.append(a)
    a = np.loadtxt("result.csv", delimiter=',')
    populationSet.append(a)
    # pool = mp.Pool()
    # info('main line')
    pset = [ ]
    for process in range(mp.cpu_count()-2):
        p = mp.Process(target=geneticOptimization, args=([s for s in populationSet],pucks,gates,process,))
        p.start()
        pset.append(p)
    
    for p in pset:
        p.join()
    # geneticOptimization(populationSet,pucks,gates)
    
    

