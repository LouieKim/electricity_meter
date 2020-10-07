# -*- coding: utf-8 -*-

class MeterCalc():
    def __init__(self):
        pass

    def electricity_calc(power_data):
        power_avg = (sum(power_data) / len(power_data)) * 55 #220v / 4(15분/60분)

        return power_avg

    def gas_calc(gas_data):
        #Todo
        pass