from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from settings import app
from flask import Flask
import json


db = SQLAlchemy(app)

class Volunteer(db.Model):

    __tablename__ = 'volunteers'
    vid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(50),nullable = False)
    role = db.Column(db.String(2), nullable=False)
    registercount = db.Column(db.Integer, nullable=False)
    scancount = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)

    def create_new_volunteer(name, username, password, is_active, role):
        new_volunteer = Volunteer(name=name, username=username, password=password, is_active=is_active, role=role)
        db.session.add(new_volunteer)
        db.session.commit()
        
    def find_by_id(id):
        return Volunteer.query.filter_by(vid = id).first()

    def find_by_username(username):
        return Volunteer.query.filter_by(username=username).first()

    def find_by_username_and_role(username, role):
        for i in role:
            my_vol = Volunteer.query.filter_by(username=username, role = i).first()
            if my_vol != None:
                return my_vol
        return None

    def find_all():
        return Volunteer.query.all()
    
    def change_status(vid, is_active):
        volunteer = Volunteer.query.filter_by(vid = vid).first()
        volunteer.is_active = is_active
        db.session.commit()

    def find_all_for_role(role):
        return Volunteer.query.filter(Volunteer.role.in_(role))

    def increment_register_count(vid):
        my_volunteer = Volunteer.query.filter_by(vid = vid).first()
        if my_volunteer.registercount == None:
            my_volunteer.registercount = 1
        else:
            my_volunteer.registercount += 1
        db.session.commit()

    def increment_scan_count(vid):
        my_volunteer = Volunteer.query.filter_by(vid = vid).first()
        if my_volunteer.scancount == None:
            my_volunteer.scancount = 1
        else:
            my_volunteer.scancount += 1
        db.session.commit()