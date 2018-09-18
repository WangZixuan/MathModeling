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
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False

gates = Gates.Gates().all_gates
pucks = Pucks.Pucks(gates=gates).all_pucks
a = np.loadtxt("result-greedy.csv", delimiter=',')


# plt.subplot(121)
# anpai = np.zeros([69,288])

# for plane in range(303):
#     try:
#         placedGate = list(a[plane][:]).index(1)
#     except:
#         placedGate = -1

#     if placedGate >= 0:
#         for index in range(pucks[plane].arrive_time,pucks[plane].depart_time):
#             if(pucks[plane].arrive_type == 'D'  and pucks[plane].depart_type=='D'):
#                 anpai[placedGate][index] = 1
#             elif(pucks[plane].arrive_type == 'D'  and pucks[plane].depart_type=='I'):
#                 anpai[placedGate][index] = 2
#             elif(pucks[plane].arrive_type == 'I'  and pucks[plane].depart_type=='D'):
#                 anpai[placedGate][index] = 3
#             elif(pucks[plane].arrive_type == 'I'  and pucks[plane].depart_type=='I'):
#                 anpai[placedGate][index] = 4

# list1 = [[],[]]
# list2 = [[],[]]
# list3 = [[],[]]
# list4 = [[],[]]

# #[d,d] 1
# #[d,i] 2
# #[i,d] 3
# #[i,i] 4

# for index1 in range(anpai.shape[0]):
#     for index2 in range(anpai[index1][:].shape[0]):
#         if anpai[index1][index2] > 0:
#             if anpai[index1][index2] == 1:
#                 list1[0].append(index1)
#                 list1[1].append(index2)
            
#             if anpai[index1][index2] ==2:
#                 list2[0].append(index1)
#                 list2[1].append(index2)

#             if anpai[index1][index2] == 3:
#                 list3[0].append(index1)
#                 list3[1].append(index2)
            
#             if anpai[index1][index2] == 4:
#                 list4[0].append(index1)
#                 list4[1].append(index2)

# l1= plt.scatter(list1[0], list1[1], marker='.',color='black')
# l2  = plt.scatter(list2[0], list2[1], marker='.',color='yellow')
# l3= plt.scatter(list3[0], list3[1], marker='.',color='green')
# l4 = plt.scatter(list4[0], list4[1], marker='.',color='red')
# plt.axis([-0.5, 69.5, 0, 350])
# plt.legend(handles=[l1, l2,l3,l4], labels=[u'国内到达/国内出发', u'国内到达/国际出发',u'国际到达/国内出发',u'国际到达/国际出发'],  loc='best')
    

# plt.subplot(122)

anpai = np.zeros([303,288])
klist = [[],[]]

for plane in range(303):
    try:
        placedGate = list(a[plane][:]).index(1)
    except:
        placedGate = -1

    if placedGate < 0:
        for index in range(pucks[plane].arrive_time,pucks[plane].depart_time):
            if(pucks[plane].arrive_type == 'D'  and pucks[plane].depart_type=='D'):
                anpai[plane][index] = 1
            elif(pucks[plane].arrive_type == 'D'  and pucks[plane].depart_type=='I'):
                anpai[plane][index] = 2
            elif(pucks[plane].arrive_type == 'I'  and pucks[plane].depart_type=='D'):
                anpai[plane][index] = 3
            elif(pucks[plane].arrive_type == 'I'  and pucks[plane].depart_type=='I'):
                anpai[plane][index] = 4
        if pucks[plane].flight_type == 1:
            klist[0].append(plane)
            klist[1].append(315)



list1 = [[],[]]
list2 = [[],[]]
list3 = [[],[]]
list4 = [[],[]]

#[d,d] 1
#[d,i] 2
#[i,d] 3
#[i,i] 4

for index1 in range(anpai.shape[0]):
    for index2 in range(anpai[index1][:].shape[0]):
        if anpai[index1][index2] > 0:
            if anpai[index1][index2] == 1:
                list1[0].append(index1+1)
                list1[1].append(index2)
            
            if anpai[index1][index2] ==2:
                list2[0].append(index1+1)
                list2[1].append(index2)

            if anpai[index1][index2] == 3:
                list3[0].append(index1+1)
                list3[1].append(index2)
            
            if anpai[index1][index2] == 4:
                list4[0].append(index1+1)
                list4[1].append(index2)

l1= plt.scatter(list1[0], list1[1], marker='.',color='black',s=10)
l2  = plt.scatter(list2[0], list2[1], marker='.',color='yellow',s=10)
l3= plt.scatter(list3[0], list3[1], marker='.',color='green',s=10)
l4 = plt.scatter(list4[0], list4[1], marker='.',color='red',s=10)
# plt.axis([-0.5, 69.5, 0, 350])
# l5 = plt.scatter(klist[0], klist[1], marker='.',color='red')

#
plt.legend(handles=[l1, l2,l3,l4], labels=[u'国内到达/国内出发', u'国内到达/国际出发',u'国际到达/国内出发',u'国际到达/国际出发'],  loc='best',ncol=2)
print(klist[0])
plt.axis([-0.5, 303, 0, 350])


# for index in range(69):
    # if gates[index].arrive_type_D == 1:
          
plt.show()
