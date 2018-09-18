#coding:utf-8
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
import matplotlib
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False

gates = Gates.Gates().all_gates
pucks = Pucks.Pucks(gates=gates).all_pucks
a = np.loadtxt("opt.csv", delimiter=',')

anpai = np.zeros([69,288])

for plane in range(303):
    try:
        placedGate = list(a[plane,:]).index(1)
    except:
        placedGate = -1

    if placedGate >= 0:
        for index in range(pucks[plane].arrive_time,pucks[plane].depart_time):
            if(pucks[plane].arrive_type == 'D'  and pucks[plane].depart_type=='D'):
                anpai[placedGate,index] = 1
            elif(pucks[plane].arrive_type == 'D'  and pucks[plane].depart_type=='I'):
                anpai[placedGate,index] = 2
            elif(pucks[plane].arrive_type == 'I'  and pucks[plane].depart_type=='D'):
                anpai[placedGate,index] = 3
            elif(pucks[plane].arrive_type == 'I'  and pucks[plane].depart_type=='I'):
                anpai[placedGate,index] = 4

klist = [[],[]]
klist1 = [[],[]]
klist2 = [[],[]]
klist3 = [[],[]]
klist4 = [[],[]]

for index in range(69):
    if gates[index].flight_type == 1:
        klist[0].append(index+1)
        klist[1].append(315)
    if gates[index].arrive_type_D == 1 and gates[index].depart_type_D == 1 :
        klist1[0].append(index+1)
        klist1[1].append(320)
    if gates[index].arrive_type_D == 1 and gates[index].depart_type_I == 1 :
        klist2[0].append(index+1)
        klist2[1].append(325)
    if gates[index].arrive_type_I == 1 and gates[index].depart_type_D == 1 :
        klist3[0].append(index+1)
        klist3[1].append(330)
    if gates[index].arrive_type_I == 1 and gates[index].depart_type_I == 1 :
        klist4[0].append(index+1)
        klist4[1].append(335)


       

#[d,d] 1
#[d,i] 2
#[i,d] 3
#[i,i] 4

list1 = [[],[]]
list2 = [[],[]]
list3 = [[],[]]
list4 = [[],[]]

for index1 in range(anpai.shape[0]):
    for index2 in range(anpai[index1,:].shape[0]):
        if anpai[index1,index2] > 0:
            if anpai[index1,index2] == 1:
                list1[0].append(index1+1)
                list1[1].append(index2)
            
            if anpai[index1,index2] ==2:
                list2[0].append(index1+1)
                list2[1].append(index2)

            if anpai[index1,index2] == 3:
                list3[0].append(index1+1)
                list3[1].append(index2)
            
            if anpai[index1,index2] == 4:
                list4[0].append(index1+1)
                list4[1].append(index2)




l1= plt.scatter(list1[0], list1[1], marker='.',color='black')
l2  = plt.scatter(list2[0], list2[1], marker='.',color='yellow')
l3= plt.scatter(list3[0], list3[1], marker='.',color='green')
l4 = plt.scatter(list4[0], list4[1], marker='.',color='red')
#
# l5 = plt.scatter(klist1[0], klist1[1], marker='.',color='black')
# l6 = plt.scatter(klist2[0], klist2[1], marker='.',color='yellow')
# l7 = plt.scatter(klist3[0], klist3[1], marker='.',color='green')
# l8 = plt.scatter(klist4[0], klist4[1], marker='.',color='red')

# l9 = plt.scatter(klist[0], klist[1], marker='.',color='blue')

plt.axis([-0.5, 69.5, 0, 330])
plt.legend(handles=[l1, l2,l3,l4], labels=[u'国内到达/国内出发', u'国内到达/国际出发',u'国际到达/国内出发',u'国际到达/国际出发'],  loc='best',ncol=2)
matplotlib.rc('xtick', labelsize=10)     
matplotlib.rc('ytick', labelsize=10)
# ax.tick_params(direction='out', length=6, width=2, colors='r',grid_color='r', grid_alpha=0.5)

# SMALL_SIZE = 8
# MEDIUM_SIZE = 10
# BIGGER_SIZE = 12

# plt.rc('font', size=BIGGER_SIZE)          # controls default text sizes
# plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
# plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
# plt.rc('xtick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
# plt.rc('ytick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
# plt.rc('legend', fontsize=BIGGER_SIZE)    # legend fontsize
# plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

plt.show()
# for i in range(288):
    # print('.')




    