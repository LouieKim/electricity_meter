from pymodbus.client.sync import ModbusTcpClient as ModbusClient

import logging
from logging import handlers

from flask import Flask, jsonify, redirect, url_for, request
from flask_cors import CORS,cross_origin

from contextlib import closing
import sqlite3
import json

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import and_, func
from meter_calc import MeterCalc
from model import ModbusPointInfo

import psutil

import platform
import setproctitle

import subprocess

from gems_modbus import GemsModbus

def main():
    #_LOGGER.error("aaa")
    app.run(host="localhost", port="5000")

if __name__ == "__main__":
    main()
    
    #aa = model_modbus_info()
    #print(aa[0].get_description())