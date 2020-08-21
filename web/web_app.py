from flask import Flask, render_template
import sqlite3
import json
import platform
import setproctitle

app = Flask(__name__)

@app.route('/')
def chart():
    return render_template('chart.html')    

@app.route('/test')
def test_chart():
    return render_template('chart_test01.html')    

if __name__ == '__main__':
    if platform.system() == "Linux":
        setproctitle.setproctitle('ninewatt_web')

    app.run(host="0.0.0.0", port="7070", debug=True)

    print("======Done=====")