import Pucks
import Gates
import checkFeasibility
import numpy as np
import compare_func


def puck_compare_stay_time(puck1, puck2):
    stay1 = puck1.depart_time - puck1.arrive_time
    stay2 = puck2.depart_time - puck2.arrive_time
    return stay1 - stay2


def initialize(pucks, gates):
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

    pucks_copy = [s for s in pucks]

    pucks_copy.sort(key=compare_func.cmp_to_key(puck_compare_stay_time))

    allocation_result = np.zeros((len(pucks_copy), len(gates)))
    for i in range(0, len(pucks_copy)):
        for j in range(0, len(gates)):
            allocation_result[pucks_copy[i].id, j] = int(1)
            if checkFeasibility.check_feasibility(allocation_result, pucks, gates):
                print("{}-{}".format(pucks_copy[i].id, j))
                break
            else:
                allocation_result[pucks_copy[i].id, j] = 0

    return allocation_result


if __name__ == "__main__":
    g = Gates.Gates().all_gates
    p = Pucks.Pucks(gates=g).all_pucks

    # result = initialize(p, g)
    # np.savetxt("result.csv", result, fmt="%d", delimiter=',')
    # print(checkFeasibility.check_feasibility(result, p, g))

    result_greedy = initialize_greedy(p, g)
    np.savetxt("result-greedy.csv", result_greedy, fmt="%d", delimiter=',')
    print(checkFeasibility.check_feasibility(result_greedy, p, g))
