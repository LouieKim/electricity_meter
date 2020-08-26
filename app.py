from pymodbus.client.sync import ModbusTcpClient as ModbusClient

import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
#logging.basicConfig(format=FORMAT)
#log = logging.getLogger()
#log.setLevel(logging.DEBUG)

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

# configuration
DATABASE = 'ninewatt_bems.db'

app = Flask(__name__)
CORS(app, support_credentials=True)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE
db = SQLAlchemy(app)

def connect_db():
    return sqlite3.connect(DATABASE)

def init_db():
    #Rerefence: https://flask-ptbr.readthedocs.io/en/latest/tutorial/dbinit.html
    with closing(connect_db()) as db:    
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read().decode('utf-8'))
        db.commit()

class ModbusInfo(db.Model):
    point_id = db.Column(db.Integer, primary_key=True)
    slave = db.Column(db.Integer, nullable=False)
    function_code = db.Column(db.Integer, nullable=False)
    map_address = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(50), nullable=False)

class History(db.Model):
    point_id = db.Column(db.Integer, db.ForeignKey('modbus_info.point_id', ondelete='CASCADE'))
    date = db.Column(db.DateTime, default=datetime.now, primary_key=True)
    value = db.Column(db.Integer, nullable=False)

class CalcHistory(db.Model):
    point_id = db.Column(db.Integer, db.ForeignKey('modbus_info.point_id', ondelete='CASCADE'))
    date = db.Column(db.DateTime, primary_key=True)
    value = db.Column(db.Integer, nullable=False)

@app.route('/polling')
def get_modbus_value():

    rows = ModbusInfo.query.all()

    for row in rows:
        raw_modbus_value = GemsModbus.read_device_map(row.slave, row.map_address)
        
        job_query = History(point_id = row.point_id, value = raw_modbus_value)

        db.session.add(job_query)
        db.session.commit()

    return "success"

#Average per 5 Minutes
#Param: start_date -> 2008041315
#Param: end_date -> 2008041330

@app.route('/calc/<start_date>/<end_date>')
def calc_data_graph(start_date, end_date):

    length = 2
    tmp_txt = [start_date[i:i+length] for i in range(0, len(start_date), length)]
    str_dt_txt = "20" + tmp_txt[0] + "-" + tmp_txt[1] + "-" + tmp_txt[2] + " " + tmp_txt[3] + ":" + tmp_txt[4] + ":00"

    tmp_txt = [end_date[i:i+length] for i in range(0, len(end_date), length)]
    end_dt_txt = "20" + tmp_txt[0] + "-" + tmp_txt[1] + "-" + tmp_txt[2] + " " + tmp_txt[3] + ":" + tmp_txt[4] + ":00"

    modbus_info_dates = ModbusInfo.query.all()

    for info_date in modbus_info_dates:

        power_list = list()
        
        history_datas = History.query.filter(and_(History.date >= str_dt_txt, History.date < end_dt_txt, History.point_id == info_date.point_id)).all()
        
        for history_data in history_datas:
            power_list.append(history_data.value)

        #print(power_list)
        
        watt_avg = MeterCalc.electricity_calc(power_list)
        watt_avg_int = round(watt_avg)

        date_time_obj = datetime.strptime(end_dt_txt, "%Y-%m-%d %H:%M:%S")

        job_query = CalcHistory(point_id = info_date.point_id, date = date_time_obj, value = watt_avg_int)
        db.session.add(job_query)
        db.session.commit()

    return "succss"


def model_modbus_info():
    rows = ModbusInfo.query.all()

    tmp_list = list()
    point_list = list()

    for row in rows:
        tmp_list = [row.point_id, row.slave, row.function_code, row.map_address, row.description]
        point_list.append(ModbusPointInfo(tmp_list))
    
    return point_list

@app.route('/realtime')
def get_real_time_data():
    #raw_real_time = History.query(History.point_id, func.max(History.date)).group_by(History.point_id).scalar()
    raw_real_time = History.query.with_entities(History.point_id, func.max(History.date), History.value).group_by(History.point_id).all()
    #Reference: https://leilayanhui.gitbooks.io/teachmyselfpython/content/Chap5/note/ch5_7_insert_select.html
    #raw_real_time = History.query.group_by(History.point_id).all()
    #raw_real_time = History.query.all()
    #raw_real_time = db.session.query(History.point_id, func.max(History.date), History.value).group_by(History.point_id).all()

    result_list = list()
    
    for row in raw_real_time:
        result_dict = dict()
        result_dict['point_id'] = row.point_id
        result_dict['value'] = row.value
        result_list.append(result_dict)
    
    dict_rows = {"data" : result_list}
    dict_rows_json = json.dumps(dict_rows)

    return dict_rows_json

@app.route('/resource')
def get_resource():
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory()[2]  # physical memory usage
    hdd_percent = psutil.disk_usage('/')[3]

    resource_dict = {'cpu': cpu_percent, 'mem': mem_percent, 'hdd': hdd_percent}
    resource_json = json.dumps(resource_dict)

    return resource_json

@app.route('/process')
def get_process():

    result_status = dict()

    app_status  = "ninewatt_app" in (p.name() for p in psutil.process_iter())
    manager_status = "ninewatt_manager" in (p.name() for p in psutil.process_iter())
    web_status  = "ninewatt_web" in (p.name() for p in psutil.process_iter())

    result_status["ninewatt_app"] = app_status
    result_status["ninewatt_manager"] = manager_status
    result_status["ninewatt_web"] = web_status 

    dict_rows_json = json.dumps(result_status)
    
    return dict_rows_json

@app.route('/timenow')
def get_timenow():
    
    time_dict = dict()

    now = datetime.now()

    nowDatetime = now.strftime('%Y-%m-%d %H:%M')
    #print(type(nowDatetime))
    time_dict["time"] = nowDatetime[2:]

    dict_rows_json = json.dumps(time_dict)

    return dict_rows_json

@app.route('/modbusinfo')
def get_modbus_info():
    
    result_list = list()
    
    modbus_info_dates = ModbusInfo.query.all()

    for info_date in modbus_info_dates:
        result_status = dict()
        result_status["point_id"] = info_date.point_id
        result_status["slave"] = info_date.slave
        result_status["function_code"] = info_date.function_code
        result_status["map_address"] = info_date.map_address
        result_status["unit"] = info_date.unit
        result_list.append(result_status)
    
    dict_rows = {"modbus_info" : result_list}  
    dict_rows_json = json.dumps(dict_rows)

    return dict_rows_json

# @app.route('/modbus/delete/<int:point_id>')
# def del_modbus_info(point_id):

#     post = ModbusInfo.query.get_or_404(point_id)
#     db.session.delete(post)
#     db.session.commit()

#     return "success"

@app.route('/modbus/delete', methods = ['GET', 'POST'])
def abab():

    if request.method == 'POST':
        req_point_id = request.form['point_id']

        post = ModbusInfo.query.get_or_404(req_point_id)
        db.session.delete(post)
        db.session.commit()

        resp = jsonify(success=True)
        return resp

@app.route('/modbus/new', methods = ['GET', 'POST'])
def new_modbus_info():
    if request.method == 'POST':
        req_slave = request.form['slave']
        req_code = request.form['function_code']
        req_address = request.form['map_address']
        req_unit = request.form['unit']

        job_query = ModbusInfo(slave = req_slave, function_code = req_code, map_address = req_address, unit = req_unit)

        db.session.add(job_query)
        db.session.commit()

        resp = jsonify(success=True)
        return resp

    else:
        return "success"

@app.route('/process/stop')
def process_stop():
    subprocess.call("supervisorctl stop ninewatt_manager")
    return "success"

@app.route('/process/start')
def process_start():
    subprocess.call("supervisorctl start ninewatt_manager")
    return "success"

"""
DATE_TIME = "00:00:00"

@app.route('/historydata/<get_date>')
def get_history(get_date):
    #raw_history_data = History.query.filter_by(date=get_date).all()

    length = 2
    test = [get_date[i:i+length] for i in range(0, len(get_date), length)]
    
    get_date = "20" + test[0] + "-" + test[1] + "-" + test[2] + " " + DATE_TIME

    raw_history_data = History.query.filter(History.date >= get_date).all()

    bb = list()

    for row in raw_history_data:
        a = [row.point_id, row.date.strftime('%Y-%m-%d %H:%M:%S'), row.value]
        bb.append(a)

    dict_rows = {"data" : bb}
    dict_rows_json = json.dumps(dict_rows)
    
    return dict_rows_json

@app.route('/graph/<point_id>/<start_date>/<end_date>')
def get_history_graph(point_id, start_date, end_date):
    #Select Data From Graph History Table

    length = 2
    a = [start_date[i:i+length] for i in range(0, len(start_date), length)]
    str_dt_txt = "20" + a[0] + "-" + a[1] + "-" + a[2] + " " + a[3] + ":" + a[4] + ":00"

    b = [end_date[i:i+length] for i in range(0, len(end_date), length)]
    end_dt_txt = "20" + b[0] + "-" + b[1] + "-" + b[2] + " " + b[3] + ":" + b[4] + ":00"

    raw_history_data = GraphHistory.query.filter(and_(GraphHistory.date >= str_dt_txt, GraphHistory.date < end_dt_txt, GraphHistory.point_id == point_id)).all()
    
    bb = list()

    for row in raw_history_data:
        a = [row.point_id, row.date.strftime('%Y-%m-%d %H:%M:%S'), row.value]
        bb.append(a)

    dict_rows = {"data" : bb}
    dict_rows_json = json.dumps(dict_rows)
    
    return dict_rows_json


@app.route('/graphdata/<send_date>')
def get_graph_history(send_date):
    #Select Data From Graph History Table
    
    length = 2
    a = [send_date[i:i+length] for i in range(0, len(send_date), length)]
    send_date_txt = "20" + a[0] + "-" + a[1] + "-" + a[2] + " " + a[3] + ":" + a[4] + ":00"

    end_dt_txt = "20" + a[0] + "-" + a[1] + "-" + a[2] + " " + a[3] + ":" + a[4] + ":01"

    raw_history_data = GraphHistory.query.filter(and_(GraphHistory.date >= send_date_txt, GraphHistory.date < end_dt_txt)).all()
    
    bb = dict()

    bb["date"] = send_date_txt

    for row in raw_history_data:
        if row.point_id == 1:
            bb["ampere"] = row.value

        elif row.point_id == 2:
            bb["ac_pwr"] = row.value
        
        elif row.point_id == 3:
            bb["re_pwr"] = row.value
        
        elif row.point_id == 4:
            bb["ap_pwr"] = row.value

        elif row.point_id == 5:
            bb["watt"] = row.value

    dict_rows = bb
    dict_rows_json = json.dumps(dict_rows)
    
    return dict_rows_json
"""

def main():
    app.run(host="localhost", port="5000", debug=True)

if __name__ == "__main__":
    init_db()

    if platform.system() == "Linux":
        setproctitle.setproctitle('ninewatt_app')
    
    main()

    
    #aa = model_modbus_info()
    #print(aa[0].get_description())