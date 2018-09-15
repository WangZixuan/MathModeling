import numpy as np
import Pucks
import Gates


def cmp_to_key(mycmp):
    '''
    Convert a cmp= function into a key= function
    :param mycmp:
    :return:
    '''
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K


def puck_compare(puck1, puck2):
    return puck1.arrive_time - puck2.arrive_time


def check_feasibility(allocation, pucks, gates):
    '''
    Check feasibility for the allocation
    :param allocation: an M*N matrix,
                        (i, j) = 1 means puck i is allocated to gate j,
                        M means the size of the pucks,
                        N means the size of the Gates.
    :param pucks: all pucks
    :param gates: all gates
    :return: True if this allocation is feasible
    '''

    [rows, cols] = allocation.shape

    indexes = []

    for i in range(0, rows):
        allocation_i = allocation[i, :]

        # if each puck is allocated once and only once
        if np.sum(allocation_i) != 1:
            return False
        for j in range (0, cols):
            if allocation_i[j] == 1:
                indexes.append(j)
                break

    # if this puck's flight_type/arrive_type/depart_type meet the gate's
    for i in range(0, rows):

        puck_i = pucks[i]
        gate_i = gates[indexes[i]]

        if puck_i.arrive_type == 'D' and gate_i.arrive_type_D == 0:
            return False

        if puck_i.arrive_type == 'I' and gate_i.arrive_type_I == 0:
            return False

        if puck_i.depart_type == 'D' and gate_i.depart_type_D == 0:
            return False

        if puck_i.depart_type == 'I' and gate_i.depart_type_I == 0:
            return False

        if puck_i.flight_type != gate_i.flight_type:
            print(puck_i.flight_type)
            print(gate_i.flight_type)
            print(i)
            return False

    # check if a 45min gap is ok
    for i in range(0, cols):
        puck_at_gate = []
        for j in range(0, rows):
            if allocation[j, i] == 1:
                puck_at_gate.append(pucks[j])

        # check now
        puck_at_gate.sort(key=cmp_to_key(puck_compare))

        for j in range(0, len(puck_at_gate)-1):
            if puck_at_gate[j].depart_time + 9 > puck_at_gate[j+1].arrive_time:
                return False

    return True


if __name__ == '__main__':
    p = Pucks.Pucks()
    g = Gates.Gates()
    a = [[0, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 1, 0, 0, 0, 0, 0]
         ]
    print(check_feasibility(np.array(a), p.all_pucks, g.all_gates))
