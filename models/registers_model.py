from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
from settings import app
import json


db = SQLAlchemy(app)

class Registers(db.Model):
    
    __tablename__ = 'registers'

    id = db.Column(db.Integer, primary_key=True)
    vid = db.Column(db.Integer,nullable=False)
    pid = db.Column(db.Integer, nullable=False)
    days = db.Column(db.Integer, default = 0)
    ends = db.Column(db.Integer, default = 0)
    weeks = db.Column(db.Integer, default = 0)
    tstamp = db.Column(db.DateTime, nullable = False)

    def log_for_register(vid, pid, days, ends, weeks):
        my_log = Registers(vid = vid, pid = pid, days = days, ends = ends, weeks = weeks, tstamp = datetime.now())
        db.session.add(my_log)
        db.session.commit()

    def find_all_pass_registers():
        return Registers.query.order_by(Registers.tstamp.desc()).all()

    def find_volunteer_registers(vid):
        return Registers.query.filter_by(vid = vid).order_by(Registers.tstamp.desc()).all()

    def find_customer_registers(pid):
        return Registers.query.filter_by(pid = pid).order_by(Registers.tstamp.desc()).all()

    def find_last_three_volunteer_registers(vid):
        return Registers.query.filter_by(vid = vid).order_by(Registers.tstamp.desc()).limit(3)
        
    def find_by_id(id):
        return Registers.query.filter_by(id = id).first()

    def delete_register(id):
        Registers.query.filter_by(id = id).delete()
        db.session.commit()