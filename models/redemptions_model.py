from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from settings import app
from flask import Flask
import json


db = SQLAlchemy(app)

class Redemptions(db.Model):
    
    __tablename__ = 'redemptions'

    id = db.Column(db.Integer, primary_key=True)
    vid = db.Column(db.Integer,nullable=False)
    pid = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String, default = "d")
    qty = db.Column(db.Integer, default = 0)
    tstamp = db.Column(db.DateTime, nullable = False)

    def log_for_redemption(vid, pid, type, qty):
        my_log = Redemptions(vid = vid, pid = pid, type = type, qty = qty, tstamp = datetime.now())
        db.session.add(my_log)
        db.session.commit()

    def find_all_pass_redemptions():
        return  Redemptions.query.order_by(Redemptions.tstamp.desc()).all()

    def find_volunteer_redemptions(vid):
        return Redemptions.query.filter_by(vid = vid).order_by(Redemptions.tstamp.desc()).all()

    def find_customer_redemptions(pid):
        return Redemptions.query.filter_by(pid = pid).order_by(Redemptions.tstamp.desc()).all()

    def find_last_fifteen_volunteer_redemptions(vid):
        return Redemptions.query.filter_by(vid = vid).order_by(Redemptions.tstamp.desc()).limit(15)