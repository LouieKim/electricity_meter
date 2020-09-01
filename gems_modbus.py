# python3.8

from pymodbus.client.sync import ModbusTcpClient as ModbusClient

UNIT = 0x1
MODBUS_TCP_IP = '192.168.7.200'
MODBUS_PORT = 502

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
            client.close()

#     import time
#     import logging
#     from logging import handlers

#     LOG_FILENAME = "test_logging.log"

#     fmt = "%(asctime)s %(levelname)s (%(threadName)s) [%(name)s] %(message)s"
#     datefmt = "%Y-%m-%d %H:%M:%S"
#     logFormatter = logging.Formatter(fmt)

#     fileLogHandler = logging.FileHandler(LOG_FILENAME)
#     fileLogHandler.setFormatter(logFormatter)
#     fileLogHandler.setLevel(logging.DEBUG)
#     fileLogHandler.suffix = "%Y%m%d_%H%M%S"


#     _LOGGER = logging.getLogger(__name__)
#     _LOGGER.setLevel(logging.DEBUG)
#     _LOGGER.addHandler(fileLogHandler)

#     for i in range(10):

#         if i % 2 == 0:
#             print("aaa")
#             MODBUS_TCP_IP = '192.168.100.10'
#             GemsModbus.read_device_map(1, 137)
#         else:
#             print("bbb")
#             MODBUS_TCP_IP = '192.168.100.200'
#             GemsModbus.read_device_map(1, 137)
        
#         time.sleep(2)
