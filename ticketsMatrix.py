'''
Get tickets matrix, which is a directional graph
'''
import Pucks
import Gates
import Tickets
import numpy as np

def get_path_matrix(pucks, tickets):
    allocation_matrix = np.zeros((len(pucks), len(pucks)))
    for one_ticket in tickets:
        arrive_name = one_ticket.arrive_flight
        depart_name = one_ticket.depart_flight

        arrive_index = -1
        depart_index = -1
        for i in range(0, len(pucks)):
            if pucks[i].arrive_flight == arrive_name:
                arrive_index = i
            if pucks[i].depart_flight == depart_name:
                depart_index = i

        if arrive_index > 0 and depart_index > 0 and arrive_index != depart_index:
            allocation_matrix[arrive_index][depart_index] += 1
    return allocation_matrix


if __name__ == '__main__':
    g = Gates.Gates().all_gates
    p = Pucks.Pucks(gates=g).all_pucks
    t = Tickets.Tickets().all_tickets
    matrix = get_path_matrix(p, t)
    print(matrix)
