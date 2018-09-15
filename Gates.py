import pandas as pd


class Gate:
    def __init__(self, gate_name, terminal,
                 area, arrive_type, depart_type, flight_type):
        self.gate_name = gate_name
        self.terminal = terminal
        self.area = area
        self.arrive_type = arrive_type
        self.depart_type = depart_type
        self.flight_type = flight_type

        if arrive_type.find('D') >= 0:
            self.arrive_type_D = 1
        else:
            self.arrive_type_D = 0

        if arrive_type.find('I') >= 0:
            self.arrive_type_I = 1
        else:
            self.arrive_type_I = 0

        if depart_type.find('D') >= 0:
            self.depart_type_D = 1
        else:
            self.depart_type_D = 0

        if depart_type.find('I') >= 0:
            self.depart_type_I = 1
        else:
            self.depart_type_I = 0


class Gates:
    def __init__(self):
        self.all_gates = []
        data_frame = pd.read_excel('InputData.xlsx', sheet_name=2)
        for index in data_frame.index:
            d = data_frame.loc[index].values[:]

            flight_type = 0
            if d[5]=='W':
                flight_type = 1

            g = Gate(d[0], d[1], d[2], d[3], d[4], flight_type)
            self.all_gates.append(g)

        print(self.all_gates)


if __name__ == '__main__':
    g = Gates()
