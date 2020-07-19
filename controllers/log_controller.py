from responses import StandardResponseBody, DataRetrievalBody
from models import Passes, Registers, Redemptions, Volunteer
from helpers.excel_helper import create_passes_excel
from flask import Response, jsonify, send_file
from datetime import date
from settings import app
import pytz


def map_register(register, volunteer_name_mapper):
    if register != None:
        #register.tstamp.replace(tzinfo=pytz.timezone('Asia/Kolkata'))
        return {
            'id': str(register.id),
            'days': str(register.days),
            'ends': str(register.ends),
            'weeks': str(register.weeks),
            'tstamp': str(register.tstamp),
            'registered_by': volunteer_name_mapper[register.vid]
        }

def map_redemption(redemption, volunteer_name_mapper):
    if redemption != None:
        return {
            'type': redemption.type,
            'qty': redemption.qty,
            'tstamp': str(redemption.tstamp),
            'redeemed_by': volunteer_name_mapper[redemption.vid]
        }

def get_details_by_phone(phone):
     
    volunteers = Volunteer.find_all()

    volunteer_name_mapper = dict()
    for volunteer in volunteers:
        volunteer_name_mapper[volunteer.vid] = volunteer.name

    my_pass = Passes.find_by_phone(phone)
    if my_pass == None:
        return jsonify(StandardResponseBody('Error', "Invalid mobile number entered").to_dict()),400
    
    pid = my_pass.pid
    
    list_register = [ map_register(i, volunteer_name_mapper) for i in Registers.find_customer_registers(pid)]
    list_redeem = [ map_redemption(i, volunteer_name_mapper) for i in Redemptions.find_customer_redemptions(pid)]

    customer_info = {
        'name': my_pass.name,
        'phone': my_pass.phone,
        'amount': my_pass.amount,
        'url': my_pass.url,
    }

    data = {
        'register_details': list_register,
        'redemption_details': list_redeem
    }

    return jsonify( DataRetrievalBody('Success', 'Customer data successfully retrieved', customer_info, data).to_dict())

def create_excel_for_passes():
    create_passes_excel()

    response = send_file("all_passes_excel.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    return response
    
def get_all_logs():

    volunteers = Volunteer.find_all()

    volunteer_name_mapper = dict()
    for volunteer in volunteers:
        volunteer_name_mapper[volunteer.vid] = volunteer.name
    
    print(volunteer_name_mapper)

    list_register = [ map_register(i, volunteer_name_mapper) for i in Registers.find_all_pass_registers()]
    list_redeem = [ map_redemption(i, volunteer_name_mapper) for i in Redemptions.find_all_pass_redemptions()]

    data = {
        'register_details': list_register,
        'redemption_details': list_redeem
    }

    return jsonify( DataRetrievalBody('Success', 'Customer data successfully retrieved', {}, data).to_dict())
