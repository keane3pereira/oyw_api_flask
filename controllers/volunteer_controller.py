from responses import GetAllVolunteersResponseBody, StandardResponseBody
from sms_templates import get_sms_for_newly_created_volunteer
from helpers.sms_helper import send_transactional_sms
from models import Volunteer, Registers, Redemptions
from flask import jsonify


def get_all_volunteers(user_data):

    role_map = {
        'ar': ['ar','r'],
        'as': ['as','s']
    }

    volunteers = []
    if user_data['role'] == 'sa':
        volunteers = Volunteer.find_all()
    else:
        volunteers = Volunteer.find_all_for_role(role_map[user_data['role']])
    
    volunteer_mapper = lambda volunteer: {
        'vid': volunteer.vid,
        'name': volunteer.name,
        'username': volunteer.username,
        'role': volunteer.role,
        'is_active': volunteer.is_active
    }

    volunteers_to_return = list(map(volunteer_mapper, volunteers))
    return jsonify(GetAllVolunteersResponseBody('Success', 'Volunteers successfully retrieved', volunteers_to_return).to_dict())


def create_volunteer(admin_id, name, username, password, is_active, role):

    my_volunteer = Volunteer.find_by_username(username)
    if my_volunteer != None:
        return jsonify(StandardResponseBody('Error', 'Username already exists').to_dict())

    Volunteer.create_new_volunteer(name, username, password, is_active, role)
     
    message = get_sms_for_newly_created_volunteer(name)#print(message)
    data = send_transactional_sms(username, message)#print(data)

    return jsonify(StandardResponseBody('Success', 'Successfully created volunteer').to_dict())

def set_volunteer_status(user_data, vid, is_active):
    Volunteer.change_status(vid, is_active)
    return jsonify(StandardResponseBody('Success', 'Successfully changed volunteer status').to_dict())



