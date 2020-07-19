from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, Response, jsonify
import routes.volunteer_routes as volunteer_routes
from helpers.auth_helper import reset_temp_tokens
import routes.auth_routes as auth_routes
import routes.pass_routes as pass_routes
import routes.log_routes as log_routes
from models import Passes
from settings import *
import atexit


@app.route('/volunteers', methods=['GET'])
def get_all_volunteers(): return volunteer_routes.get_all_volunteers(['as','ar'], True)

@app.route('/volunteers', methods=['POST'])
def create_volunteer(): return volunteer_routes.create_volunteer(['ar','as'], True)

@app.route('/volunteers/<int:vid>/status', methods=['PATCH'])
def set_volunteer_status(vid): return volunteer_routes.set_volunteer_status(['ar','as'], True, vid)

@app.route('/login', methods = ['POST'])
def login(): return auth_routes.login()

@app.route('/register', methods=['POST'])
def register(): return pass_routes.register_pass(['ar','r'],False)

@app.route('/scan_pass', methods = ['POST','GET'])
def scan_day_pass(): return pass_routes.scan_pass(['as','s'],False)

@app.route('/accept_pass', methods = ['POST', 'GET'])
def accept_pass(): return pass_routes.accept_pass(['as','s'],False)

@app.route('/display_codes', methods=['POST','GET'])
def display_codes(): return pass_routes.get_qrs()

@app.route('/download_pass', methods=['POST','GET'])
def download_pass(): return pass_routes.download_pass()

@app.route('/get_all_customer_transactions', methods = ['POST'])
def get_all_customer_transactions(): return log_routes.get_all_customer_transactions([],False)

@app.route('/get_all_logs', methods = ['GET'])
def get_all_logs(): return log_routes.get_all_logs([],False)

@app.route('/resend_url', methods = ['POST', 'GET'])
def resend_url(): return pass_routes.resend_url()

@app.route('/create_passes_excel', methods = ['POST'])
def create_excel_for_pass(): return log_routes.create_passes_excel(['ar'],False)

@app.route('/delete_register', methods = ['POST'])
def delete_register(): return pass_routes.delete_register([], True)

scheduler = BackgroundScheduler()

scheduler.add_job(func = reset_temp_tokens, trigger = "cron", hour = "04", minute = "00" )
scheduler.add_job(func=Passes.reset_weekscanned, trigger = "cron", hour = '03', minute = '00')

scheduler.start()
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False, port=5379)
