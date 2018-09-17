import Gates
import Pucks
import numpy as np
import checkFeasibility
import compare_func
import initialize
import random


def repair(allocation, pucks, gates):
    '''
    repair the allocation matrix which is non-feasible(may be generated from Genetic Algorithm).
    :param allocation: allocation matrix which is non-feasible
    :param pucks: all pucks.
    :param gates: all gates
    :return: new allocation matrix guaranteed to be feasible
    '''

    if checkFeasibility.check_feasibility(allocation, pucks, gates):
        return allocation

    [rows, cols] = allocation.shape

    for i in range(0, rows):
        allocation_i = allocation[i, :]

        # if each puck is allocated at most once
        if np.sum(allocation_i) > 1:
            assert False

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

                if random.random() < 0.7:
                    allocation[puck_at_gate[j + 1].id, i] = 0
                    del puck_at_gate[j + 1]
                else:
                    allocation[puck_at_gate[j].id, i] = 0
                    del puck_at_gate[j]
                flag = 1
            j = j + 1
            if flag == 1:
                j = 0

    assert checkFeasibility.check_feasibility(allocation, pucks, gates)

    # place those who are misses

    pucks_at_gate = [[] for i in range(0, cols)]

    for i in range(0, cols):
        for j in range(0, rows):
            if allocation[j, i] == 1:
                pucks_at_gate[i].append(pucks[j])

    pucks_copy = [s for s in pucks]

    for i in range(0, len(pucks_copy)):
        allocation_i = allocation[pucks_copy[i].id, :]
        if np.sum(allocation_i) == 0:

            available = pucks[pucks_copy[i].id].available_gates

            for a in range(0, len(available)):
                pucks_existed = pucks_at_gate[available[a]]

                pucks_existed_copy = [s for s in pucks_existed]
                pucks_existed_copy.append(pucks[pucks_copy[i].id])

                # check if ok
                can_change = 1

                pucks_existed_copy.sort(key=compare_func.cmp_to_key(initialize.puck_compare_stay_time))

                for j in range(0, len(pucks_existed_copy) - 1):
                    if pucks_existed_copy[j].depart_time + 9 > pucks_existed_copy[j + 1].arrive_time:
                        can_change = 0
                        break

                if can_change == 1:
                    allocation[pucks_copy[i].id, available[a]] = 1
                    # print("insert {} to gate {}".format(pucks_copy[i].id, available[a]))
                    pucks_at_gate[available[a]].append(pucks[pucks_copy[i].id])
                    # print(checkFeasibility.check_feasibility(allocation, p, g))

                    break

    return allocation


if __name__ == '__main__':
    g = Gates.Gates().all_gates
    p = Pucks.Pucks(gates=g).all_pucks
    a = np.loadtxt("test.csv", delimiter=',')
    a = repair(a, p, g)
    print(checkFeasibility.check_feasibility(a, p, g))
