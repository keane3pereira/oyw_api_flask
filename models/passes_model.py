from flask_sqlalchemy import SQLAlchemy
from hashlib import sha256, sha1
from time import localtime
from settings import app
from flask import Flask
import json


db = SQLAlchemy(app)

class Passes(db.Model):
    
    __tablename__ = 'passes'
    pid = db.Column('pid', db.Integer, primary_key=True)
    name = db.Column('name', db.String(20))
    phone = db.Column('phone', db.String(10), nullable=False)
    url = db.Column('url', db.String(100), nullable=False)
    daycode = db.Column('daycode', db.String(50), nullable=False)
    weekcode = db.Column('weekcode', db.String(50), nullable=False)
    days = db.Column('days', db.Integer, default=0)
    ends = db.Column('ends', db.Integer, default=0)
    weeks = db.Column('weeks', db.Integer, default=0)
    weekscanned = db.Column('weekscanned', db.Integer, default=0)
    amount = db.Column('amount', db.Integer, default=0)

    def find_all():
        return Passes.query.all()

    def find_by_id(pid):
        return Passes.query.filter_by(pid = pid).first()

    def find_by_phone(phone):
        return Passes.query.filter_by(phone = phone).first()

    def find_by_daycode(daycode):
        return Passes.query.filter_by(daycode = daycode).first()

    def find_by_weekcode(weekcode):
        return Passes.query.filter_by(weekcode = weekcode).first()
        
    def find_by_url(url):
        return Passes.query.filter_by(url = url).first()

    def create_new_pass(name,phone):

        url = sha1(bytes(phone, encoding='utf-8')).hexdigest()
        daycode = sha256(bytes('oyw'+phone+'d', encoding='utf-8')).hexdigest()
        weekcode = sha256(bytes('oyw'+phone+'w', encoding='utf-8')).hexdigest()
        new_pass = Passes(name=name,phone=phone,url=url,daycode=daycode,weekcode=weekcode)
        
        db.session.add(new_pass)
        db.session.commit()

    def register_pass_by_phone(phone, days, ends, weeks):

        my_pass = Passes.query. filter_by(phone = phone).first()
        my_pass.days += int(days)
        my_pass.ends += int(ends)
        my_pass.weeks += int(weeks)
    
        amt = int(days) * 30 + int(ends) * 50 + int(weeks) * 200
        my_pass.amount += amt
        db.session.commit()

    def accept_by_phone(type, phone, qty):

        my_pass = Passes.query.filter_by(phone = phone).first()

        if type == 'd':
            if localtime()[2] < app.config['DATE_FASHION_SHOW']:
                my_pass.days -= int(qty)
            else:
                my_pass.ends -= int(qty)

        elif type == 'w':
            my_pass.weekscanned += int(qty)

        db.session.commit()

    def reset_weekscanned():
        Passes.query.update({Passes.weekscanned: 0}) 
        db.session.commit()

    def get_total_weekscanned():
        return sum( [i.weekscanned for i in Passes.query.all()] )

    def undo_register(pid, days, ends, weeks):
    
        my_pass = Passes.query. filter_by(pid = pid).first()
        my_pass.days -= int(days)
        my_pass.ends -= int(ends)
        my_pass.weeks -= int(weeks)
    
        amt = int(days) * 30 + int(ends) * 50 + int(weeks) * 200
        my_pass.amount -= amt
        db.session.commit()