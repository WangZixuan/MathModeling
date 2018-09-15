import pandas as pd
import time

WideBody = (['332', '333', '33E', '33H', '33L', '773'])


class Puck:
    def __init__(self, id,
                 arrive_date, arrive_time, arrive_flight, arrive_type,
                 flight_id,
                 depart_date, depart_time, depart_flight, depart_type
                 ):
        self.id = id
        self.flight_id = flight_id

        self.flight_type = 0
        if flight_id in WideBody:
            self.flight_type = 1

        if arrive_date == 19:
            self.arrive_time = 0
        else:
            self.arrive_time = arrive_time.hour * 12 + arrive_time.min / 5
        self.arrive_flight = arrive_flight
        self.arrive_type = arrive_type

        if depart_date == 21:
            self.depart_time = 24 * 12
        else:
            self.depart_time = depart_time.hour * 12 + arrive_time.min / 5
        self.depart_flight = depart_flight
        self.depart_type = depart_type


class Pucks:

    def __init__(self):
        self.all_pucks = []
        data_frame = pd.read_excel('InputData.xlsx')
        for index in data_frame.index:
            d = data_frame.loc[index].values[:]

            p = Puck(d[0], d[12], d[2], d[3], d[4], str(d[5]), d[13], d[7], d[8], d[9])
            # print(p)
            self.all_pucks.append(p)
        # print(self.all_pucks)


if __name__ == '__main__':
    p = Pucks()
