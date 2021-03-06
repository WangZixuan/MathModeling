'''
Count passengers' transfer time.
'''

import Gates
import Tickets
import Pucks
import numpy as np
import math
import checkFeasibility
import compare_func

# walking time table
WalkingTime = {
    'TN-TN': 2, 'TN-TC': 3, 'TN-TS': 4, 'TN-SN': 5, 'TN-SC': 4, 'TN-SS': 5, 'TN-SE': 5,
    'TC-TN': 3, 'TC-TC': 2, 'TC-TS': 3, 'TC-SN': 4, 'TC-SC': 3, 'TC-SS': 4, 'TC-SE': 4,
    'TS-TN': 4, 'TS-TC': 3, 'TS-TS': 2, 'TS-SN': 5, 'TS-SC': 4, 'TS-SS': 5, 'TS-SE': 5,
    'SN-TN': 5, 'SN-TC': 4, 'SN-TS': 5, 'SN-SN': 2, 'SN-SC': 3, 'SN-SS': 4, 'SN-SE': 4,
    'SC-TN': 4, 'SC-TC': 3, 'SC-TS': 4, 'SC-SN': 3, 'SC-SC': 2, 'SC-SS': 3, 'SC-SE': 3,
    'SS-TN': 5, 'SS-TC': 4, 'SS-TS': 5, 'SS-SN': 4, 'SS-SC': 3, 'SS-SS': 2, 'SS-SE': 4,
    'SE-TN': 5, 'SE-TC': 4, 'SE-TS': 5, 'SE-SN': 4, 'SE-SC': 3, 'SE-SS': 4, 'SE-SE': 2,
}

# paperwork time table
PaperWorkTime = {
    'DT-DT': 3, 'DT-DS': 4, 'DT-IT': 7, 'DT-IS': 8,
    'DS-DT': 4, 'DS-DS': 3, 'DS-IT': 8, 'DS-IS': 7,
    'IT-DT': 7, 'IT-DS': 8, 'IT-IT': 4, 'IT-IS': 6,
    'IS-DT': 8, 'IS-DS': 9, 'IS-IT': 6, 'IS-IS': 4,
}

# MRT round times
MRTRound = {
    'DT-DT': 0, 'DT-DS': 1, 'DT-IT': 0, 'DT-IS': 1,
    'DS-DT': 1, 'DS-DS': 0, 'DS-IT': 1, 'DS-IS': 0,
    'IT-DT': 0, 'IT-DS': 1, 'IT-IT': 0, 'IT-IS': 1,
    'IS-DT': 1, 'IS-DS': 2, 'IS-IT': 1, 'IS-IS': 0,
}


def compare_transfer_time(pair1, pair2):
    if pair1[3] is None or pair1[2] is None or pair2[3] is None or pair2[2] is None:
        return 0
    transfer_user_time1 = pair1[3] - pair1[2]
    transfer_user_time2 = pair2[3] - pair2[2]
    return transfer_user_time1 - transfer_user_time2


def transfer_gates(allocation, gates, tickets, pucks):
    '''
    :param allocation:
    :param gates:
    :param tickets:
    :param pucks:
    :return: tickets_gates pairs in the form
            [arrive_gate_id, depart_gate_id,
            arrive_time, depart_time,
            arrive_type, depart_type
            passengers_num, ticket_id]
    '''
    tickets_gates = []

    for ticket_i in range(0, len(tickets)):
        this_ticket = tickets[ticket_i]
        this_ticket_arrive_gate = -1
        this_ticket_depart_gate = -1
        this_ticket_arrive_time = None
        this_ticket_depart_time = None
        this_ticket_arrive_type = None
        this_ticket_depart_type = None

        # which flight it is
        for i in range(0, len(pucks)):
            if pucks[i].arrive_flight == this_ticket.arrive_flight:
                allocation_i = allocation[i, :]
                this_ticket_arrive_time = pucks[i].arrive_time
                this_ticket_arrive_type = pucks[i].arrive_type
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
                this_ticket_depart_time = pucks[i].depart_time
                this_ticket_depart_type = pucks[i].depart_type
                if this_ticket.depart_date == 21:
                    this_ticket_depart_time += 24*12

                # which gate is allocated to this flight
                for j in range(0, len(gates)):
                    if allocation_i[j] == 1:
                        this_ticket_depart_gate = gates[j].id
                        break
                break

        tickets_gates.append([this_ticket_arrive_gate, this_ticket_depart_gate,
                              this_ticket_arrive_time, this_ticket_depart_time,
                              this_ticket_arrive_type, this_ticket_depart_type,
                              this_ticket.passengers_num, this_ticket.id])

    return tickets_gates


def transfer_time_2(allocation, gates, tickets, pucks):
    '''

    :param allocation:
    :param gates:
    :param tickets:
    :param pucks:
    :return: transfer_time in the form of (size of tickets, 1)
    '''
    assert checkFeasibility.check_feasibility(allocation, pucks, gates)
    pairs = transfer_gates(allocation, gates, tickets, pucks)

    transfer_time_all = []

    count = 0

    for i in range(0, len(pairs)):

        if pairs[i][0] < 0 or pairs[i][1] < 0:
            continue

        if pairs[i][2] is None or pairs[i][3] is None:
            continue

        arrive_gate = gates[pairs[i][0]]
        depart_gate = gates[pairs[i][1]]

        identifier_terminal = pairs[i][4] + arrive_gate.terminal + '-' + pairs[i][5] + depart_gate.terminal

        # print("{}-{}".format(pairs[i][2], pairs[i][3]))

        if pairs[i][2] + PaperWorkTime[identifier_terminal] <= pairs[i][3]:
            transfer_time_temp = pairs[i][6] * PaperWorkTime[identifier_terminal]
            transfer_time_all.append(transfer_time_temp)
            count += pairs[i][6]
        else:
            transfer_time_all.append(-1)



    return count, transfer_time_all


def transfer_time_3(allocation, gates, tickets, pucks):
    '''

    :param allocation:
    :param gates:
    :param tickets:
    :param pucks:
    :return: transfer_time in the form of (size of tickets, 2)
    '''
    assert checkFeasibility.check_feasibility(allocation, pucks, gates)
    pairs = transfer_gates(allocation, gates, tickets, pucks)
    # pairs.sort(key=compare_func.cmp_to_key(compare_transfer_time))

    transfer_time_all = []

    count = 0

    for i in range(0, len(pairs)):

        if pairs[i][0] < 0 or pairs[i][1] < 0:
            continue

        if pairs[i][2] is None or pairs[i][3] is None:
            continue

        arrive_gate = gates[pairs[i][0]]
        depart_gate = gates[pairs[i][1]]

        identifier_terminal = pairs[i][4] + arrive_gate.terminal + '-' + pairs[i][5] + depart_gate.terminal

        identifier_area = arrive_gate.terminal + arrive_gate.area[0] + '-' + depart_gate.terminal + depart_gate.area[0]

        # print("{}-{}".format(pairs[i][2], pairs[i][3]))

        used_time = PaperWorkTime[identifier_terminal] + WalkingTime[identifier_area] + \
                    math.ceil(MRTRound[identifier_terminal] * 1.6)
        if pairs[i][2] + used_time <= pairs[i][3]:
            transfer_time_temp = pairs[i][6] * used_time
            transfer_time_all.append(transfer_time_temp)
            count += pairs[i][6]
        else:
            transfer_time_all.append(-1)

    return count, transfer_time_all


def generate_matrix(allocation, pucks, gates):
    '''
    TODO useless function
    :param allocation:
    :param pucks:
    :param gates:
    :return:
    '''

    F = np.zeros([303,303])
    for i in range(303):
        if allocation[i,:].sum() == 0:
            continue
        index1 = pucks[i].arrive_type
        index2 = gates[list(allocation[i, :]).index(1)].terminal
        index5 = gates[list(allocation[i, :]).index(1)].area
        for j in range(303):
            if allocation[j,:].sum() == 0:
                continue
            index3 = pucks[j].depart_type
            index4 = gates[list(allocation[j, :]).index(1)].terminal
            index6 = gates[list(allocation[j, :]).index(1)].area
            # print(allocation[j,:].sum())
            # print(index1,index2,index3,index4)
            temp = PaperWorkTime[index1+index2+'-'+index3+index4]
            temp += WalkingTime[index2+index5[0]+'-'+index4+index6[0]]
            temp += math.ceil(MRTRound[index1+index2+'-'+index3+index4] * 1.6)

            F[i, j] = temp

    return F


def generate_puck_to_puck_matrix(pucks):
    '''

    :param pucks:
    :return:
    '''
    puck_to_puck_matrix = np.zeros([303, 303])
    for i in range(0, 303):
        arr_t = pucks[i].arrive_time
        for j in range(0, 303):
            dep_t = pucks[j].depart_time

            if arr_t + 9 < dep_t:
                puck_to_puck_matrix[i, j] = dep_t - arr_t
    return puck_to_puck_matrix


# test main function
if __name__ == '__main__':
    g = Gates.Gates().all_gates
    t = Tickets.Tickets().all_tickets
    p = Pucks.Pucks(g).all_pucks
    a = np.loadtxt("opt.csv", delimiter=',')
    # tt2 = transfer_time_2(a, g, t, p)
    # tt3 = transfer_time_3(a, g, t, p)

    # generate_matrix(a, p, g)

    generate_puck_to_puck_matrix(p)
