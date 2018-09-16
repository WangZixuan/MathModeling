import pandas as pd


class Ticket:
    def __init__(self, id, passengers_num, arrive_flight, arrive_date,
                 depart_flight, depart_date):
        self.id = id
        self.passengers_num = passengers_num
        self.arrive_flight = arrive_flight
        self.arrive_date = arrive_date
        self.depart_flight = depart_flight
        self.depart_date = depart_date


class Tickets:
    def __init__(self):
        self.all_tickets = []

        data_frame = pd.read_excel('InputData.xlsx', sheet_name=1)
        for index in data_frame.index:
            d = data_frame.loc[index].values[:]

            t = Ticket(d[0], d[2], d[3], d[7], d[5], d[8])
            # print(t)
            self.all_tickets.append(t)


if __name__ == '__main__':
    t = Tickets()
