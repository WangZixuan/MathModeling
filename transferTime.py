import Gates
import Tickets
import Pucks
import numpy as np
import checkFeasibility

WalkingTime = {
    'TN-TN': 2, 'TN-TC': 3, 'TN-TS': 4, 'TN-SN': 5, 'TN-SC': 4, 'TN-SS': 5, 'TN-SE': 5,
    'TC-TN': 3, 'TC-TC': 2, 'TC-TS': 3, 'TC-SN': 4, 'TC-SC': 3, 'TC-SS': 4, 'TC-SE': 4,
    'TS-TN': 4, 'TS-TC': 3, 'TS-TS': 2, 'TS-SN': 5, 'TS-SC': 4, 'TS-SS': 5, 'TS-SE': 5,
    'SN-TN': 5, 'SN-TC': 4, 'SN-TS': 5, 'SN-SN': 2, 'SN-SC': 3, 'SN-SS': 4, 'SN-SE': 4,
    'SC-TN': 4, 'SC-TC': 3, 'SC-TS': 4, 'SC-SN': 3, 'SC-SC': 2, 'SC-SS': 3, 'SC-SE': 3,
    'SS-TN': 5, 'SS-TC': 4, 'SS-TS': 5, 'SS-SN': 4, 'SS-SC': 3, 'SS-SS': 2, 'SS-SE': 4,
    'SE-TN': 5, 'SE-TC': 4, 'SE-TS': 5, 'SE-SN': 4, 'SE-SC': 3, 'SE-SS': 4, 'SE-SE': 2,
}


def transfer_gates(allocation, gates, tickets, pucks):
    '''

    :param allocation:
    :param gates:
    :param tickets:
    :param pucks:
    :return: tickets_gates pairs in the form
            [arrive_gate_id, depart_gate_id, arrive_time, depart_time, passengers_num]
    '''
    tickets_gates = []

    for ticket_i in range(0, len(tickets)):
        this_ticket = tickets[ticket_i]
        this_ticket_arrive_gate = -1
        this_ticket_depart_gate = -1
        this_ticket_arrive_time = None
        this_ticket_depart_time = None

        # which flight it is
        for i in range(0, len(pucks)):
            if pucks[i].arrive_flight == this_ticket.arrive_flight:
                allocation_i = allocation[i, :]
                this_ticket_arrive_time = pucks[i].arrive_time
                if this_ticket.arrive_date == 19:
                    this_ticket_arrive_time -= 24*12

                # which gate is allocated to this flight
                for j in range(0, len(gates)):
                    if allocation_i[j] == 1:
                        this_ticket_arrive_gate = gates[j].id
                        break
                break

        for i in range(0, len(pucks)):
            if pucks[i].depart_flight == this_ticket.depart_flight:
                allocation_i = allocation[i, :]
                this_ticket_depart_time = pucks[i].arrive_time
                if this_ticket.depart_date == 21:
                    this_ticket_depart_time += 24*12

                # which gate is allocated to this flight
                for j in range(0, len(gates)):
                    if allocation_i[j] == 1:
                        this_ticket_depart_gate = gates[j].id
                        break
                break

        tickets_gates.append([this_ticket_arrive_gate, this_ticket_depart_gate, this_ticket_arrive_time, this_ticket_depart_time, this_ticket.passengers_num])

    return tickets_gates


def transfer_walking_time(allocation, gates, tickets, pucks):
    assert checkFeasibility.check_feasibility(allocation, pucks, gates)
    pairs = transfer_gates(allocation, gates, tickets, pucks)

    walking_time = 0

    failed_passengers = 0

    for i in range(0, len(pairs)):

        if pairs[i][0] < 0 or pairs[i][1] < 0:
            continue

        if pairs[i][2] is None or pairs[i][3] is None:
            continue

        arrive_gate = gates[pairs[i][0]]
        depart_gate = gates[pairs[i][1]]

        identifier = arrive_gate.terminal + arrive_gate.area[0] + '-' + depart_gate.terminal + depart_gate.area[0]

        if pairs[i][2] + WalkingTime[identifier] <= pairs[i][3]:
            walking_time += pairs[i][4] * WalkingTime[identifier]
        else:
            failed_passengers += 1

    # print(walking_time)
    return walking_time, failed_passengers


if __name__ == '__main__':
    g = Gates.Gates().all_gates
    t = Tickets.Tickets().all_tickets
    p = Pucks.Pucks(g).all_pucks
    a = np.loadtxt("result-greedy.csv", delimiter=',')
    wt, fp = transfer_walking_time(a, g, t, p)
    print(wt)
    print(fp)
