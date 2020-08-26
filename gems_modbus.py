# python3.8

from pymodbus.client.sync import ModbusTcpClient as ModbusClient

UNIT = 0x1
MODBUS_TCP_IP = '192.168.7.164'
MODBUS_PORT = 502

class GemsModbus():
    def __init__(self):
        pass

    def read_device_map(slave, map_address):
        try:
            client = ModbusClient(MODBUS_TCP_IP, port=MODBUS_PORT)
            client.connect()

            gems_value = client.read_input_registers(map_address, slave, unit=UNIT)

        except Exception as e:
            #print(e)
            return "Fail Connecting Device"
        
        finally :
            client.close()
            return gems_value.registers[0]