'''
Generate data with given form from allocation matrix.
@Author Zixuan Wang
@Date 2018/9/16
'''

import Pucks
import Gates
import numpy as np
import checkFeasibility


# main function
if __name__ == '__main__':
    g = Gates.Gates().all_gates
    p = Pucks.Pucks(g).all_pucks

    allocation = np.loadtxt("opt2.csv", delimiter=',')

    print(checkFeasibility.check_feasibility(allocation, p, g))

    [rows, cols] = allocation.shape

    with open("final2.csv", "w") as f:
        f.write("飞机转场记录号,登机口\n")
        for i in range(0, rows):
            allocation_i = allocation[i,:]
            j = 0
            while j < cols:
                if allocation_i[j] == 1:
                    break
                j = j + 1

            # print("{}-{}".format(i, j))
            if j != cols:
                f.write(p[i].record_num + "," + g[j].gate_name + "\n")

    anpai = np.zeros([69, 288])

    for plane in range(303):
        try:
            placedGate = list(allocation[plane, :]).index(1)
        except:
            placedGate = -1

        if placedGate >= 0:
            for index in range(p[plane].arrive_time, p[plane].depart_time):
                if (p[plane].arrive_type == 'D' and p[plane].depart_type == 'D'):
                    anpai[placedGate, index] = 1
                elif (p[plane].arrive_type == 'D' and p[plane].depart_type == 'I'):
                    anpai[placedGate, index] = 1
                elif (p[plane].arrive_type == 'I' and p[plane].depart_type == 'D'):
                    anpai[placedGate, index] = 1
                elif (p[plane].arrive_type == 'I' and p[plane].depart_type == 'I'):
                    anpai[placedGate, index] = 1

  
    list1 = [[], []]
    for i in range(69):
        list1[0].append(i)
        list1[1].append(anpai[i, :].sum() / 288.0)
        
    with open("final-gates2.csv", "w") as f:
        f.write("Gate-Name,飞机\n")
        for i in range(0, cols):
            allocation_i = allocation[:, i]
            j = 0
            feiji = []
            while j < rows:
                if allocation_i[j] == 1:
                    feiji.append(p[j].record_num)
                j += 1
            f.write(g[i].gate_name)

            f.write("," + str(len(feiji)))
            f.write("," + str(list1[1][i]))

            [f.write(","+x) for x in feiji]

            f.write("\n")

