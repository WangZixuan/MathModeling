'''
Initialize a random solution
'''

import Pucks
import Gates
import Tickets
import checkFeasibility
import numpy as np
import compare_func
import operator


def puck_compare_stay_time(puck1, puck2):
    '''
    Compare two pucks based on their stay time, used in sort function.
    :param puck1:
    :param puck2:
    :return:
    '''
    stay1 = puck1.depart_time - puck1.arrive_time
    stay2 = puck2.depart_time - puck2.arrive_time
    return stay1 - stay2


def puck_compare_depart_and_stay_time(puck1, puck2):
    '''
    Compare two pucks based on their depart and stay time, used in sort function.
    :param puck1:
    :param puck2:
    :return:
    '''
    if puck1.depart_time == puck2.depart_time:
        stay1 = puck1.depart_time - puck1.arrive_time
        stay2 = puck2.depart_time - puck2.arrive_time
        return stay1 - stay2
    return puck1.depart_time - puck2.depart_time


def initialize(pucks, gates):
    '''
    Initialize based on index starting from 0.
    :param pucks:
    :param gates:
    :return: allocation matrix
    '''
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


def initialize_greedy(pucks, gates):
    '''
    Initialize starting from least stay time.
    :param pucks:
    :param gates:
    :return: allocation matrix
    '''

    pucks_copy = [s for s in pucks]

    pucks_copy.sort(key=compare_func.cmp_to_key(puck_compare_depart_and_stay_time))

    allocation_result = np.zeros((len(pucks_copy), len(gates)))
    for i in range(0, len(pucks_copy)):
        for j in range(len(gates) -1, -1, -1):
            allocation_result[pucks_copy[i].id, j] = int(1)
            if checkFeasibility.check_feasibility(allocation_result, pucks, gates):
                print("{}-{}".format(pucks_copy[i].id, j))
                break
            else:
                allocation_result[pucks_copy[i].id, j] = 0

    return allocation_result


def initialize_for_passengers(pucks, gates, tickets, want_path_matrix=False):
    '''
    A greedy way to make passengers walk least
    :param pucks:
    :param gates:
    :param tickets:
    :param want_path_matrix:
    :return: allocation matrix
    '''

    flight_names = set()

    for p in pucks:
        if p.arrive_flight[0] != '*':
            flight_names.add(p.arrive_flight)
        if p.depart_flight[0] != '*':
            flight_names.add(p.depart_flight)

    for ti in tickets:
        if ti.arrive_flight not in flight_names:
            flight_names.add(ti.arrive_flight)
        if ti.depart_flight not in flight_names:
            flight_names.add(ti.depart_flight)

    path_matrix = np.zeros((len(flight_names), len(flight_names)))

    flight_names_arr = list(flight_names)

    for ti in tickets:
        arr_f = flight_names_arr.index(ti.arrive_flight)
        dep_f = flight_names_arr.index(ti.depart_flight)
        path_matrix[arr_f][dep_f] += ti.passengers_num

    if want_path_matrix:
        return flight_names_arr, path_matrix

    flight_usage = {}
    for f in flight_names_arr:
        flight_usage[f] = 0

    for i in range(0, len(flight_names_arr)):
        for j in range(0, len(flight_names_arr)):
            flight_usage[flight_names_arr[i]] += path_matrix[i][j]
            flight_usage[flight_names_arr[j]] += path_matrix[i][j]

    sorted_flight_usage = sorted(flight_usage.items(), key=operator.itemgetter(1), reverse=True)

    allocation_result = np.zeros((len(pucks), len(gates)))

    for flight_item in sorted_flight_usage:

        # search this item
        for i in range(0, len(pucks)):
            flag = False
            if pucks[i].arrive_flight == flight_item[0] or pucks[i].depart_flight == flight_item[0]:
                available = pucks[i].available_gates

                while len(available) != 0:
                    choice = np.random.choice(available)
                    available.remove(choice)
                    allocation_result[i, choice] = 1
                    if checkFeasibility.check_feasibility(allocation_result, pucks, gates):
                        print("{}-{}".format(i, choice))
                        flag = True
                        break
                    else:
                        allocation_result[i, choice] = 0

            if flag:
                break

    return allocation_result


# main function
if __name__ == "__main__":
    g = Gates.Gates().all_gates
    p = Pucks.Pucks(gates=g).all_pucks
    t = Tickets.Tickets().all_tickets

    # result = initialize(p, g)
    # np.savetxt("result.csv", result, fmt="%d", delimiter=',')
    # print(checkFeasibility.check_feasibility(result, p, g))

    result_greedy = initialize_greedy(p, g)
    np.savetxt("result-greedy.csv", result_greedy, fmt="%d", delimiter=',')
    print(checkFeasibility.check_feasibility(result_greedy, p, g))

    # result_passengers = initialize_for_passengers(p, g, t)
    # np.savetxt("result-passengers.csv", result_passengers, fmt="%d", delimiter=',')
    # print(checkFeasibility.check_feasibility(result_passengers, p, g))
