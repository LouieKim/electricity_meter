UNIT = 0x1
MODBUS_TCP_IP = '192.168.10.200'
MODBUS_PORT = 502

import os

NINEWATT_DB = 'ninewatt_bems.db'

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, NINEWATT_DB))
SQLALCHEMY_TRACK_MODIFICATIONS = False

REQUIRED_PYTHON_VER = (3, 7, 0)

RELEASE_VERSION = '1.2.0'