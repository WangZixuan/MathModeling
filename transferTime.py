import Gates
import Tickets
import Pucks
import numpy as np


def transfer_gates(allocation, gates, tickets, pucks):
    tickets_gates = []

    for ticket_i in range(0, len(tickets)):
        this_ticket = tickets[ticket_i]
        this_ticket_arrive_gate = -1
        this_ticket_depart_gate = -1

        # which flight it is
        for i in range(0, len(pucks)):
            if pucks[i].arrive_flight == this_ticket.arrive_flight:
                allocation_i = allocation[i, :]
                # which gate is allocated to this flight
                for j in range(0, len(gates)):
                    if allocation_i[j] == 1:
                        this_ticket_arrive_gate = gates[j].id
                        break
                break

        for i in range(0, len(pucks)):
            if pucks[i].depart_flight == this_ticket.depart_flight:
                allocation_i = allocation[i, :]
                # which gate is allocated to this flight
                for j in range(0, len(gates)):
                    if allocation_i[j] == 1:
                        this_ticket_depart_gate = gates[j].id
                        break
                break

        tickets_gates.append([this_ticket_arrive_gate, this_ticket_depart_gate])

    return tickets_gates


if __name__ == '__main__':
    g = Gates.Gates().all_gates
    t = Tickets.Tickets().all_tickets
    p = Pucks.Pucks(g).all_pucks
    a = np.loadtxt("result-greedy.csv", delimiter=',')
    tg = transfer_gates(a, g, t, p)
    print(1)
