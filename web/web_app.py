from flask import Flask, render_template
import sqlite3
import json
import platform
import setproctitle

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('chart_offline.html')

@app.route('/test')
def test_chart():
    return render_template('test03.html')

@app.route('/chart/offline')
def chart_offline():
    return render_template('chart_offline.html')

@app.route('/chart/online')
def chart_online():
    return render_template('chart_online.html')

@app.route('/setting')
def setting_modbus_info():
    return render_template('setting_offline.html')

@app.route('/setting/offline')
def setting_modbus_info_offline():
    return render_template('setting_offline.html')

@app.route('/graph/online')
def graph_chart_online():
    return render_template('graph_online.html')

@app.route('/graph/offline')
def graph_chart_offline():
    return render_template('graph_offline.html')

@app.route('/graph/test')
def graph_chart_offline_test():
    return render_template('graph_offline_test01.html')

@app.route('/chart/test')
def chart_offline_test():
    return render_template('chart_offline_test01.html')

#aaaaaaaaaaaaaaaa TESTESTEST

if __name__ == '__main__':
    if platform.system() == "Linux":
        setproctitle.setproctitle('ninewatt_web')

    app.run(host="localhost", port="7070")

    #print("======Done=====")