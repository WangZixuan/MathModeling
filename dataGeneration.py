import Pucks
import Gates
import numpy as np

if __name__ == '__main__':
    g = Gates.Gates().all_gates
    p = Pucks.Pucks(g).all_pucks

    allocation = np.loadtxt("result-greedy.csv", delimiter=',')

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
