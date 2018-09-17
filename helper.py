'''
Helper functions for Simulated Annealing
@Author Zixuan Wang
@Date 2018/9/17
'''

import Pucks
import Gates
import compare_func
import numpy as np
import checkFeasibility


def can_add(allocation, pucks, gates, index_puck, index_gate):
    '''
    Return if current allocation can add a new puck at gate
    :param allocation:
    :param pucks:
    :param gates:
    :param index_puck:
    :param index_gate:
    :return: True if add operation is possible
    '''

    allocation_i = allocation[index_puck, :]
    if np.sum(allocation_i) == 1:
        return False

    if pucks[index_puck].arrive_type == 'D' and gates[index_gate].arrive_type_D == 0:
        return False

    if pucks[index_puck].arrive_type == 'I' and gates[index_gate].arrive_type_I == 0:
        return False

    if pucks[index_puck].depart_type == 'D' and gates[index_gate].depart_type_D == 0:
        return False

    if pucks[index_puck].depart_type == 'I' and gates[index_gate].depart_type_I == 0:
        return False

    if pucks[index_puck].flight_type != gates[index_gate].flight_type:
        return False

    pucks_at_gate = []
    [rows, cols] = allocation.shape
    allocation_i = allocation[:, index_gate]
    for i in range(0, rows):
        if allocation_i[i] == 1:
            pucks_at_gate.append(pucks[i])

    pucks_at_gate.append(pucks[index_puck])

    pucks_at_gate.sort(key=compare_func.cmp_to_key(checkFeasibility.puck_compare_arrive_time))

    for j in range(0, len(pucks_at_gate)-1):
        if pucks_at_gate[j].depart_time + 9 > pucks_at_gate[j+1].arrive_time:
            return False

    return True


def add_puck(allocation, pucks, gates, index_puck, index_gate):
    '''
    add a new pucks[index_puck] to gates[index_gate]
    :param allocation:
    :param pucks:
    :param gates:
    :param index_puck:
    :param index_gate:
    :return:
    '''
    if can_add(allocation, pucks, gates, index_puck, index_gate):
        allocation[index_puck][index_gate] = 1
        return True, allocation
    return False, allocation


def delete_puck(allocation, index_puck):
    '''
    Delete pucks[index_puck] to gates[index_gate]
    :param allocation:
    :param index_puck:
    :return:
    '''

    allocation_i = allocation[index_puck, :]
    index_gate = allocation_i.index(1)
    assert np.sum(allocation_i) == 1

    if allocation[index_puck][index_gate] == 1:
        allocation[index_puck][index_gate] = 0
        return True, allocation
    return False, allocation


# test main function
if __name__ == '__main__':
    g = Gates.Gates().all_gates
    p = Pucks.Pucks(gates=g).all_pucks
    a = np.loadtxt("result-greedy.csv", delimiter=',')
    print(can_add(a, p, g, 0, 0))
