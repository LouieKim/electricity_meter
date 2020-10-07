from flask import Flask, render_template
import sqlite3
import json
import platform
import setproctitle

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('chart.html')

@app.route('/chart')
def chart():
    return render_template('chart.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/setting')
def setting():
    return render_template('setting.html')

if __name__ == '__main__':
    if platform.system() == "Linux":
        setproctitle.setproctitle('ninewatt_web')

    app.run(host="localhost", port="7070", debug="true")

    #print("======Done=====")