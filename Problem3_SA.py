from initialize import *
'''
Autor: tenk
Problem two solution file
'''

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
from ticketsMatrix import *
from transferTime import *

# 生成时间费用矩阵
def generate_puck_to_puck_matrix(pucks):
    '''

    :param pucks:
    :return:
    '''
    puck_to_puck_matrix = np.zeros([303, 303])
    for i in range(0, 303):
        arr_t = pucks[i].arrive_time
        for j in range(0, 303):
            dep_t = pucks[j].depart_time
            if dep_t - arr_t<=0:
                puck_to_puck_matrix[i, j] = 0
            else:
                puck_to_puck_matrix[i, j] = 1.0/(dep_t - arr_t)
    return puck_to_puck_matrix

g = Gates.Gates().all_gates
p = Pucks.Pucks(gates=g).all_pucks
t = Tickets.Tickets().all_tickets
pp = generate_puck_to_puck_matrix(p)
matrix = get_path_matrix(p, t)

global F
# 生成当前的评价矩阵
def score(allocation,pucks,gates):
    F = np.zeros([303,303])
    for i in range(303):
        if allocation[i,:].sum() == 0:
            continue
        index1 = pucks[i].arrive_type
        index2 = gates[list(allocation[i, :]).index(1)].terminal
        index5 = gates[list(allocation[i, :]).index(1)].area
        for j in range(303):
            
            if allocation[j,:].sum() == 0:
                continue
            index3 = pucks[j].depart_type
            index4 = gates[list(allocation[j, :]).index(1)].terminal
            index6 = gates[list(allocation[j, :]).index(1)].area
            # print(allocation[j,:].sum())
            # print(index1,index2,index3,index4)
            temp = PaperWorkTime[index1+index2+'-'+index3+index4]
            temp += WalkingTime[index2+index5[0]+'-'+index4+index6[0]]
            assert(WalkingTime[index2+index5[0]+'-'+index4+index6[0]]>0)
            temp += math.ceil(MRTRound[index1+index2+'-'+index3+index4] * 1.6)
            F[i, j] = temp
            # print('sb',temp)
    newMatrix = copy.deepcopy(matrix)
    for i in range(303):
        if allocation[i,:].sum() == 0:
            newMatrix[i,:] = np.zeros(303)
            newMatrix[:,i] = np.zeros(303)
    print( [allocation.sum() ,(F*matrix*pp).sum() , np.sign(np.sum(allocation, axis=0)).sum(),(F*matrix*pp).sum()/newMatrix.sum()])
    return allocation.sum()- (F*matrix*pp).sum() -  np.sign(np.sum(allocation, axis=0)).sum(), [allocation.sum() ,(F*matrix*pp).sum() , np.sign(np.sum(allocation, axis=0)).sum()]


# 获取人流量矩阵
matrix = get_path_matrix(p, t)

# 策略一：邻近解获取
def transpose_1(a, pucks, gates):
    # unorder_set = list(range(303))
    s = copy.deepcopy(a)
    unassign = []
    assigned = []
    for index in range(s.shape[0]):
        if s[index,:].sum()==0:
            unassign.append(index)
        else:
            assigned.append(index)
    # gateSet = random.choice(list(range(69)),random.randint(1,3),replace=False)
    gateSet = range(10,19)
    for gate in gateSet:
        for index in range(303):
            if s[index,gate] == 1:
                unassign.append(index)
                assigned.remove(index)
    for gate in gateSet:
        s[:,gate] = np.zeros(303)
    newPucks = [ pucks[k] for k in unassign]
    newPucks.sort(key=compare_func.cmp_to_key(puck_compare_depart_and_stay_time))
    for item in newPucks:
        for index in range(68,0,-1):
            if(can_add(s,pucks,gates,item.id,index)):
                add_puck(s, pucks, gates, item.id, index)
    return s
# 策略二：邻近解获取
def transpose_2(a, pucks, gates):
    for loop in range(100):
        index1 = random.randint(0,69)
        index2 = random.randint(0,69)
        if (index1 == index2):
            continue
        if(gates[index1].flight_type != gates[index2].flight_type):
            continue
        if(gates[index1].arrive_type_D != gates[index2].arrive_type_D):
            continue
        if(gates[index1].depart_type_I != gates[index2].depart_type_I):
            continue
        tmp = copy.deepcopy(a[:,index1])
        a[:,index1] = copy.deepcopy(a[:,index2])
        a[:,index2] = copy.deepcopy(tmp)
        return a
    return a

# 策略二：模拟退火方法定义
def safunc(a,pucks,gates):
    curScore,w = score(a,pucks,gates)
    optScore,w = score(a,pucks,gates)
    optSec = w[1]
    optThi = w[1]
    maxK = 100
    T=1000 
    Tmin=10 
    k=100
    t=0
    while T >= Tmin:
        for k in range(maxK):
            # print('gg',curScore,optScore)
            newAllocation = transpose_1(a,pucks,gates)
            newAllocation = transpose_2(a,pucks,gates)
            newScore,b = score(newAllocation,pucks,gates)
            if not check_feasibility(newAllocation,pucks,gates):
                exit(-1)
            print(optScore,newAllocation.sum(),np.sign(np.sum(newAllocation, axis=0)).sum())
            if newScore > curScore:
                a = copy.deepcopy(newAllocation)
                curScore = newScore 
                if newScore > optScore or ( b[1] < optSec ):
                    
                    optScore = newScore
                    optSec   = b[1]
                    np.savetxt('opt3'+'.txt',a,fmt='%d',delimiter=',')
                    # exit(-1)
            else:
                p = math.exp(-(newScore-optScore)/T)
                r = np.random.uniform(low=0,high=1)
                if r < p:                     
                    a = copy.deepcopy(newAllocation)
                    curScore = newScore
        t+=1
        T=1000/math.log2(1+t)
# 主函数
if __name__ == '__main__':
    g = Gates.Gates().all_gates
    p = Pucks.Pucks(gates=g).all_pucks
    a = np.loadtxt("opt.csv", delimiter=',')
    safunc(a,p,g)



