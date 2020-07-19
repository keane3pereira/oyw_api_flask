from responses import StandardResponseBody, LoginResponseBody, RegisterResponseBody, DisplayResponseBody, ScanResponseBody
from sms_templates import get_register_pass_sms_template, get_accept_pass_sms_template
from graphics.format_pass import create_pass, find_created_pass_pic
from models import Volunteer, Passes, Registers, Redemptions
from helpers.firebase_helper import update_total_values
from helpers.sms_helper import send_transactional_sms
from flask import Response, jsonify, send_file
from time import localtime
from settings import app
import sms_templates
import sys
sys.path.insert(0,'helpers/')


def map_data(register):
    my_pass = Passes.find_by_id(register.pid)
    if my_pass == None or my_pass == '':
        return

    return {
        'id': register.id,
        'name': my_pass.name,
        'phone': my_pass.phone,
        'days': register.days,
        'ends': register.ends,
        'weeks': register.weeks,
        'tstamp': register.tstamp
    }

def register_pass(vid, name, phone, days, ends, weeks):
    volunteer = Volunteer.find_by_id(vid)
    if not volunteer.is_active:
        return jsonify(StandardResponseBody('Error', 'You are set as inactive').to_dict()), 400

    Volunteer.increment_register_count(vid)

    my_pass = Passes.find_by_phone(phone)
    is_new = False
    if my_pass == None:
        Passes.create_new_pass(name, phone)
        is_new = True
    else:
        name = my_pass.name    

    Passes.register_pass_by_phone(phone, days, ends, weeks)

    my_pass = Passes.find_by_phone(phone = phone)
    if my_pass == None:
        return jsonify(StandardResponseBody('Error', 'Invalid phone').to_dict()), 400

    Registers.log_for_register(vid, my_pass.pid, days, ends, weeks)

    message = get_register_pass_sms_template(name, my_pass.url)
    send_transactional_sms(phone, message)
    
    update_total_values()
    
    register_set = [ map_data(i) for i in Registers.find_last_three_volunteer_registers(vid) ]
    #print('last_three_registers', register_set)

    response = jsonify(RegisterResponseBody('Success', 'Successfully registered pass',is_new, register_set).to_dict())
    return response

def scan_pass(vid, code):
    volunteer = Volunteer.find_by_id(vid)
    if not volunteer.is_active:
        return jsonify(StandardResponseBody('Error', 'You are set as inactive').to_dict()), 400

    Volunteer.increment_scan_count(vid)

    my_pass = Passes.find_by_daycode(code)
    if my_pass == None:
        my_pass = Passes.find_by_weekcode(code)
        if my_pass == None:
            return jsonify(StandardResponseBody('Error', 'Invalid code entered').to_dict()), 400
        else:#week code
            balance = my_pass.weeks - my_pass.weekscanned
            data = {
                'name': my_pass.name,
                'phone': my_pass.phone,
                'type': 'w',
                'qty': balance
            }
    else:#day code
        if localtime()[2] < app.config['DATE_FASHION_SHOW']:
            balance = my_pass.days
        else:
            balance = my_pass.ends
        data = {
            'name': my_pass.name,
            'phone': my_pass.phone,
            'type': 'd',
            'qty': balance
        }
    response = jsonify(ScanResponseBody('Success', 'Successfully scanned pass', dict(data)).to_dict())
    return response        

def accept_pass(vol_id, type, phone, qty):

    volunteer = Volunteer.find_by_id(vol_id)
    if not volunteer.is_active:
        return jsonify(StandardResponseBody('Error', 'You are set as inactve').to_dict()), 400

    my_pass = Passes.find_by_phone(phone)
    if my_pass == None:
        return jsonify(StandardResponseBody('Error', 'Invalid pass entered').to_dict())
    else:
        print(my_pass.name)
        vol_name = Volunteer.find_by_id(vol_id).name

        Passes.accept_by_phone(type, phone, qty)

        if type == 'd':
            if localtime()[2] >= app.config['DATE_FASHION_SHOW']:
                type = 'e'
        
        Redemptions.log_for_redemption(vol_id, my_pass.pid, type, qty)

        message = get_accept_pass_sms_template(my_pass, vol_name)
        send_transactional_sms(phone, message)

        update_total_values()

        response = jsonify(StandardResponseBody('Success', 'Successfully accepted pass').to_dict())
        return response

def get_qrs(url):

    my_pass = Passes.find_by_url(url)
    if my_pass == None:
        return jsonify(StandardResponseBody('Error', 'Invalid url entered').to_dict()), 400
    codes = {
        'name': my_pass.name,
        'phone': my_pass.phone,
        'daycode': my_pass.daycode if (my_pass.days + my_pass.ends > 0) else None,
        'balance_days': my_pass.days,
        'balance_ends': my_pass.ends,
        'balance_weeks': my_pass.weeks - my_pass.weekscanned,
        'weekcode': my_pass.weekcode if my_pass.weeks != my_pass.weekscanned else None,
    }
    response = jsonify(DisplayResponseBody('Success','Successfully sent codes', dict(codes)).to_dict())
    return response

def create_pass_for_customer(url):
    my_pass = Passes.find_by_url(str(url))
    if my_pass == None:
        return jsonify(StandardResponseBody('Error', 'Invalid url code entered').to_dict()), 400

    pid = my_pass.pid
    daycode = my_pass.daycode
    weekcode = my_pass.weekcode
    name = my_pass.name.upper()

    if not find_created_pass_pic(pid):
        create_pass(pid, name, daycode,weekcode)

    response = send_file("graphics/created_passes/pass"+str(pid)+".png", mimetype='image/png')
    return response

def resend_url(phone):
    my_pass = Passes.find_by_phone(phone)
    if my_pass == None:
        return jsonify(StandardResponseBody('Error', 'Invalid mobile number entered').to_dict()), 400

    message = get_register_pass_sms_template(my_pass.name, my_pass.url)
    send_transactional_sms(phone, message)

    return jsonify(StandardResponseBody('Success', 'Successfully sent message').to_dict())

def delete_register(id):
    my_register = Registers.find_by_id(id)
    if my_register == None:
        return jsonify(StandardResponseBody('Error', 'Invalid register id').to_dict()), 400
    
    my_pass = Passes.find_by_id(my_register.pid)
    if my_pass == None:
        return jsonify(StandardResponseBody('Error', 'Invalid pass id').to_dict()), 400

    Passes.undo_register(my_register.pid, my_register.days, my_register.ends, my_register.weeks)
    Registers.delete_register(id)
    
    update_total_values()

    return jsonify(StandardResponseBody('Success', 'Successfully deleted pass').to_dict())