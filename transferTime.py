import Gates
import Tickets
import numpy as np


def transfer_time(allocation, gates, tickets):
    time_sum = 0

    for i in range(0, len(tickets)):
        this_ticket = tickets[i]


if __name__ == '__main__':
    g = Gates.Gates().all_gates
    t = Tickets.Tickets().all_tickets
    a = np.loadtxt("result-greedy.csv", delimiter=',')
    print(transfer_time(a, g, t))
