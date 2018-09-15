import Pucks
import Gates
import checkFeasibility
import numpy as np


def initialize(pucks, gates):
    allocation_result = np.zeros((len(pucks), len(gates)))
    for i in range(0, len(pucks)):

        for j in range(0, len(gates)):
            allocation_result[i, j] = int(1)
            if checkFeasibility.check_feasibility(allocation_result, pucks, gates):
                print("{}-{}".format(i, j))
                break
            else:
                allocation_result[i, j] = 0

    return allocation_result



if __name__ == "__main__":
    p = Pucks.Pucks().all_pucks
    g = Gates.Gates().all_gates
    allocation_result = initialize(p, g)
    np.savetxt("result.csv", allocation_result, fmt="%d", delimiter=',')
    print(checkFeasibility.check_feasibility(allocation_result, p, g))
