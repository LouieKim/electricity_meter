UNIT = 0x1
MODBUS_TCP_IP = '192.168.7.200'
MODBUS_PORT = 502

import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'ninewatt_bems.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

REQUIRED_PYTHON_VER = (3, 7, 0)