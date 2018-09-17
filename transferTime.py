import Gates
import Tickets
import Pucks
import numpy as np
import checkFeasibility

WalkingTime = {
    'TN-TN': 10, 'TN-TC': 15, 'TN-TS': 20, 'TN-SN': 25, 'TN-SC': 20, 'TN-SS': 25, 'TN-SE': 25,
    'TC-TN': 15, 'TC-TC': 10, 'TC-TS': 15, 'TC-SN': 20, 'TC-SC': 15, 'TC-SS': 20, 'TC-SE': 20,
    'TS-TN': 20, 'TS-TC': 15, 'TS-TS': 10, 'TS-SN': 25, 'TS-SC': 20, 'TS-SS': 25, 'TS-SE': 25,
    'SN-TN': 25, 'SN-TC': 20, 'SN-TS': 25, 'SN-SN': 10, 'SN-SC': 15, 'SN-SS': 20, 'SN-SE': 20,
    'SC-TN': 20, 'SC-TC': 15, 'SC-TS': 20, 'SC-SN': 15, 'SC-SC': 10, 'SC-SS': 15, 'SC-SE': 15,
    'SS-TN': 25, 'SS-TC': 20, 'SS-TS': 25, 'SS-SN': 20, 'SS-SC': 15, 'SS-SS': 10, 'SS-SE': 20,
    'SE-TN': 25, 'SE-TC': 20, 'SE-TS': 25, 'SE-SN': 20, 'SE-SC': 15, 'SE-SS': 20, 'SE-SE': 10,
}


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


def transfer_walking_time(allocation, gates, tickets, pucks):
    assert checkFeasibility.check_feasibility(allocation, pucks, gates)
    pairs = transfer_gates(allocation, gates, tickets, pucks)
    print(1)


if __name__ == '__main__':
    g = Gates.Gates().all_gates
    t = Tickets.Tickets().all_tickets
    p = Pucks.Pucks(g).all_pucks
    a = np.loadtxt("result-greedy.csv", delimiter=',')
    tg = transfer_walking_time(a, g, t, p)
