import Gates
import Pucks
import numpy as np
import checkFeasibility
import compare_func
import initialize


def repair(allocation, pucks, gates):
    '''
    repair the allocation matrix generated from Genetic Algorithm.
    :param allocation: allocation matrix generated from Genetic Algorithm
    :param pucks: all pucks.
    :param gates: all gates
    :return:
    '''

    if checkFeasibility.check_feasibility(allocation, pucks=p, gates=g):
        return allocation

    [rows, cols] = allocation.shape

    for i in range(0, rows):
        allocation_i = allocation[i, :]

        # if each puck is allocated at most once
        if np.sum(allocation_i) > 1:
            assert "WRONG!!!"

    for i in range(0, cols):
        puck_at_gate = []
        for j in range(0, rows):
            if allocation[j, i] == 1:
                puck_at_gate.append(pucks[j])

        puck_at_gate.sort(key=compare_func.cmp_to_key(initialize.puck_compare_stay_time))

        j = 0
        while j + 1 < len(puck_at_gate):
            flag = 0
            # check if a 45 min gap is guaranteed
            if puck_at_gate[j].depart_time + 9 > puck_at_gate[j + 1].arrive_time:
                allocation[puck_at_gate[j + 1].id, i] = 0
                puck_at_gate.remove(j + 1)
                flag = 1
                j = j + 1
            if flag == 1:
                j = 0

    print(checkFeasibility.check_feasibility(allocation,p,g))
    return allocation


if __name__ =='__main__':
    g = Gates.Gates().all_gates
    p = Pucks.Pucks(gates=g).all_pucks
    a = np.loadtxt("result.csv", delimiter=',')
    print(checkFeasibility.check_feasibility(a, p, g))