# python3.8

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import nw_logging
from config import(
    UNIT,
    MODBUS_TCP_IP,
    MODBUS_PORT
)

class GemsModbus():
    def __init__(self):
        pass

    def read_device_map(slave, map_address):
        try:
            client = ModbusClient(MODBUS_TCP_IP, port=MODBUS_PORT)
            client.connect()

            gems_value = client.read_input_registers(map_address, slave, unit=UNIT)
            
            client.close()
            return gems_value.registers[0]

        except Exception as e:
            nw_logging._LOGGER.error(e)
            client.close()