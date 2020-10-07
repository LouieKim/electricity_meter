from flask import Blueprint
from gems_modbus import GemsModbus

from model import ModbusInfo, History, CalcHistory
from meter_calc import MeterCalc
from flask import Flask, jsonify, redirect, url_for, request
from flaskr import db
from sqlalchemy import and_, func
import json
import psutil
from datetime import datetime, time, timedelta

#Reference: https://stackoverflow.com/questions/57726047/sqlalchemy-expression-language-and-sqlites-on-delete-cascade
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
import subprocess

def add_secs_to_time(timeval, secs_to_add):
    secs = timeval.hour * 3600 + timeval.minute * 60 + timeval.second
    secs += secs_to_add
    return time(secs // 3600, (secs % 3600) // 60, secs % 60)

LIST_15m_DAY = [add_secs_to_time(time(0), i).strftime("%H:%M") for i in range(0, 86400, 900)]

@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def ninewatt_hello():
    return "welcome ninewatt"

#author: hyeok0724.kim@ninewatt.com
#Update date: 20.09.18
#descript: Get meter data from GEMS 3512 or 3500 Device using MODBUS/TCP Protocol
@bp.route('/polling')
def get_modbus_value():
    try:
        rows = ModbusInfo.query.all()

        for row in rows:
            raw_modbus_value = GemsModbus.read_device_map(row.slave, row.map_address)

            #Insert History Data          
            job_query = History(point_id = row.point_id, value = raw_modbus_value)
            db.session.add(job_query)
            db.session.commit()

        return jsonify(success=True)
            
    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'get Modbus Value'}), 500

#author: hyeok0724.kim@ninewatt.com
#Update date: 20.09.18
#descript: Calculate the data saved on history table
#Param: start_date -> 2008041315, end_date -> 2008041330
@bp.route('/calc/<start_date>/<end_date>')
def calc_data_graph(start_date, end_date):
    try:
        #Convert start_date, end_date to 2020-08-01 00:00:00
        length = 2
        tmp_txt = [start_date[i:i+length] for i in range(0, len(start_date), length)]
        str_dt_txt = "20" + tmp_txt[0] + "-" + tmp_txt[1] + "-" + tmp_txt[2] + " " + tmp_txt[3] + ":" + tmp_txt[4] + ":00"

        tmp_txt = [end_date[i:i+length] for i in range(0, len(end_date), length)]
        end_dt_txt = "20" + tmp_txt[0] + "-" + tmp_txt[1] + "-" + tmp_txt[2] + " " + tmp_txt[3] + ":" + tmp_txt[4] + ":00"

        modbus_info_dates = ModbusInfo.query.all()

        for info_date in modbus_info_dates:
            history_data_list = list()      
            raw_history_data = History.query.filter(and_(History.date >= str_dt_txt, History.date < end_dt_txt, History.point_id == info_date.point_id)).all()
            
            for history_data in raw_history_data:
                history_data_list.append(history_data.value)
            
            #Calculate data selected from history
            watt_avg = MeterCalc.electricity_calc(history_data_list)
            watt_avg_int = round(watt_avg)

            date_time_obj = datetime.strptime(end_dt_txt, "%Y-%m-%d %H:%M:%S")

            job_query = CalcHistory(point_id = info_date.point_id, date = date_time_obj, value = watt_avg_int)
            db.session.add(job_query)
            db.session.commit()

        return jsonify(success=True)
    
    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'calc_data_graph'}), 500

#author: hyeok0724.kim@ninewatt.com
#Update date: 20.09.18
#descript: Get Lastest meter data from history
@bp.route('/realtime')
def get_real_time_data():
    try:
        raw_real_time = History.query.with_entities(History.point_id, func.max(History.date), History.value).group_by(History.point_id).all()

        result_list = list()
        
        for row in raw_real_time:
            result_dict = dict()
            result_dict['point_id'] = row.point_id
            result_dict['value'] = row.value
            result_list.append(result_dict)
        
        dict_rows = {"data" : result_list}
        dict_rows_json = json.dumps(dict_rows)

        return dict_rows_json

    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'get_real_time_data'}), 500

@bp.route('/resource')
def get_resource():
    try:
        cpu_percent = psutil.cpu_percent()
        mem_percent = psutil.virtual_memory()[2]  # physical memory usage
        hdd_percent = psutil.disk_usage('/')[3]

        resource_dict = {'cpu': cpu_percent, 'mem': mem_percent, 'hdd': hdd_percent}
        resource_json = json.dumps(resource_dict)

        return resource_json

    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'get_resource'}), 500

@bp.route('/process')
def get_process():
    try:
        result_status = dict()

        app_status  = "ninewatt_app" in (p.name() for p in psutil.process_iter())
        manager_status = "ninewatt_manager" in (p.name() for p in psutil.process_iter())
        web_status  = "ninewatt_web" in (p.name() for p in psutil.process_iter())

        result_status["ninewatt_app"] = app_status
        result_status["ninewatt_manager"] = manager_status
        result_status["ninewatt_web"] = web_status 

        dict_rows_json = json.dumps(result_status)

        return dict_rows_json
    
    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'get_process'}), 500

@bp.route('/timenow')
def get_timenow():
    try:
        time_dict = dict()
        now = datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M')
        time_dict["time"] = nowDatetime[2:]
        dict_rows_json = json.dumps(time_dict)

        return dict_rows_json

    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'get_timenow'}), 500

@bp.route('/modbusinfo')
def get_modbus_info():
    try:
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

        #return jsonify(dict_rows_json), 200
    
    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'Admin access is required'}), 401

@bp.route('/modbus/delete', methods = ['GET', 'POST'])
def del_modbus_info():
    try:
        if request.method == 'POST':
            req_point_id = request.form['point_id']

            post = ModbusInfo.query.get_or_404(req_point_id)
            db.session.delete(post)
            db.session.commit()

            resp = jsonify(success=True)
            return resp

    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'del_modbus_info'}), 500

@bp.route('/modbus/new', methods = ['GET', 'POST'])
def create_modbus_info():
    try:
        if request.method == 'POST':
            req_slave = request.form['slave']
            req_code = request.form['function_code']
            req_address = request.form['map_address']
            req_unit = request.form['unit']

            job_query = ModbusInfo(slave = req_slave, function_code = req_code, map_address = req_address, unit = req_unit)

            db.session.add(job_query)
            db.session.commit()

            return jsonify(success=True)

    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'create_modbus_info'}), 500

#author: hyeok0724.kim@ninewatt.com
#Update date: 20.09.18
#descript: stop manager process
@bp.route('/process/stop')
def stop_process():
    try:
        subprocess.call("supervisorctl stop ninewatt_manager", shell=True)
        return jsonify(success=True)

    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'stop_process'}), 500

#author: hyeok0724.kim@ninewatt.com
#update date: 20.09.18
#descript: start manager process
@bp.route('/process/start')
def start_process():
    try:
        subprocess.call("supervisorctl start ninewatt_manager", shell=True)
        return jsonify(success=True)

    except Exception as e:
        _LOGGER.error(e)
        print(e)
        return jsonify({'error': 'start_process'}), 500

#author: hyeok0724.kim@ninewatt.com
#update date: 20.09.18
#descript: Select Data From Graph History Table
#param: point_id, history_date -> 200801
@bp.route('/graph/<point_id>/<day_date>')
def get_history_graph(point_id, day_date):
    try:
        length = 2
        tmp_list = [day_date[i:i+length] for i in range(0, len(day_date), length)]
        str_dt_txt = "20" + tmp_list[0] + "-" + tmp_list[1] + "-" + tmp_list[2] + " 00:00:00"

        end_dt_txt = datetime.strptime(str_dt_txt, "%Y-%m-%d %H:%M:%S") + timedelta(days=1)

        raw_history_data = CalcHistory.query.filter(and_(CalcHistory.date >= str_dt_txt, CalcHistory.date < end_dt_txt, CalcHistory.point_id == point_id)).order_by(CalcHistory.date).all()

        history_data_list = list()

        for i in LIST_15m_DAY:
            tmp_data = (point_id, i, "null")
            for row in raw_history_data:
                if i == row.date.strftime('%H:%M'):
                    tmp_data = (point_id, row.date.strftime('%H:%M'), row.value)
                    break

            history_data_list.append(tmp_data)

        dict_rows_json = json.dumps(history_data_list)
        
        return dict_rows_json

    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'get_history_graph'}), 500

#author: hyeok0724.kim@ninewatt.com
#update date: 20.09.18
#descript: Select Data From Graph History Table
#param: point_id
@bp.route('/graph/<point_id>')
def get_today_history_graph(point_id):
    try:
        str_dt_txt = datetime.now().strftime('%Y-%m-%d 00:00:00')
        raw_history_data = CalcHistory.query.filter(and_(CalcHistory.date >= str_dt_txt, CalcHistory.point_id == point_id)).order_by(CalcHistory.date).all()
        
        history_data_list = list()

        for i in len(LIST_15m_DAY):
            pass

        for row in raw_history_data:
            tmp_data = (row.point_id, row.date.strftime('%H:%M'), row.value)
            history_data_list.append(tmp_data)

        dict_rows_json = json.dumps(history_data_list)
        
        return dict_rows_json
    
    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'get_today_history_graph'}), 500


#author: hyeok0724.kim@ninewatt.com
#update date: 20.09.18
#descript: Select Data From Graph History Table
#param: status
@bp.route('/xscreensaver/<status>')
def xscreensaver(status):
    if status == 'off':
        subprocess.call("xscreensaver-command -exit", shell=True)
        return jsonify({'success':"xscreensaver off"}), 200
    elif status == 'on':
        subprocess.call("xscreensaver &", shell=True)
        return jsonify({'success':"xscreensaver on"}), 200
    else:
        print("error")
        return jsonify({'error':"xscreensaver error"}), 500

@bp.route('/xscreensaver')
def xscreensaver():
    pid_check = "supervisord" in (p.name() for p in psutil.process_iter())

    if pid_check == True:
        return jsonify({'xscreensaver_status':"on"}), 200
    else:
        return jsonify({'xscreensaver_status':"off"}), 200










    