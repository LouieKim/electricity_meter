from flask import Flask, jsonify, redirect, url_for, request
from flask_cors import CORS,cross_origin
from flask_sqlalchemy import SQLAlchemy
import config
from contextlib import closing
import sqlite3

db = None

def create_app():

    global db

    app = Flask(__name__)
    app.config.from_object(__name__)
    CORS(app, support_credentials=True)

    def connect_db():
        return sqlite3.connect(config.NINEWATT_DB)

    #Rerefence: https://flask-ptbr.readthedocs.io/en/latest/tutorial/dbinit.html
    with closing(connect_db()) as db:    
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read().decode('utf-8'))
        db.commit()

    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    db = SQLAlchemy(app)

    import flaskr_routes
    app.register_blueprint(flaskr_routes.bp)

    return app