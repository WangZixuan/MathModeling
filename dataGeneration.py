'''
Generate data with given form from allocation matrix.
@Author Zixuan Wang
@Date 2018/9/16
'''

import Pucks
import Gates
import numpy as np


# main function
if __name__ == '__main__':
    g = Gates.Gates().all_gates
    p = Pucks.Pucks(g).all_pucks

    allocation = np.loadtxt("opt.csv", delimiter=',')

    [rows, cols] = allocation.shape

    with open("final.csv", "w") as f:
        f.write("飞机转场记录号,登机口\n")
        for i in range (0, rows):
            allocation_i = allocation[i,:]
            j = 0
            while j < cols:
                if allocation_i[j] == 1:
                    break
                j = j + 1

            print("{}-{}".format(i, j))
            if j != cols:
                f.write(p[i].record_num + "," + g[j].gate_name + "\n")

    with open("final-gates.csv", "w") as f:
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
            [f.write(","+x) for x in feiji]
            f.write("\n")

