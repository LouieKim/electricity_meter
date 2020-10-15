from flaskr import db
from datetime import datetime

class ModbusInfo(db.Model):
    point_id = db.Column(db.Integer, primary_key=True)
    slave = db.Column(db.Integer, nullable=False)
    function_code = db.Column(db.Integer, nullable=False)
    map_address = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(50), nullable=False)

class History(db.Model):
    point_id = db.Column(db.Integer, db.ForeignKey('modbus_info.point_id', ondelete='cascade'))
    date = db.Column(db.DateTime, default=datetime.now, primary_key=True)
    value = db.Column(db.Integer, nullable=False)

class CalcHistory(db.Model):
    point_id = db.Column(db.Integer, db.ForeignKey('modbus_info.point_id', ondelete='cascade'))
    date = db.Column(db.DateTime, default=datetime.now, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    