from helpers.auth_helper import is_user_authenticated_and_authorized, get_user_data
from flask import Flask, request, Response, jsonify, send_file
import controllers.pass_controller as pass_controller
from responses import StandardResponseBody


def register_pass(allowed_roles, is_only_for_admin):

    if 'token' not in request.headers:
        return jsonify(StandardResponseBody('Error', 'Token is a required field').to_dict()),400

    token = request.headers['token']
    if not is_user_authenticated_and_authorized(token, allowed_roles, is_only_for_admin):
        return jsonify(StandardResponseBody('Error', 'User is not authorized to perform this operation').to_dict()), 401
    user_data = get_user_data(token)

    if 'phone' not in request.form:
        return jsonify(StandardResponseBody('Error', 'Phone number is a required field').to_dict()),400
    elif 'days' not in request.form:
        return jsonify(StandardResponseBody('Error', 'Number of day passes is a required field').to_dict()),400
    elif 'ends' not in request.form:
        return jsonify(StandardResponseBody('Error', 'Number of end passes  is a required field').to_dict()),400
    elif 'weeks' not in request.form:
        return jsonify(StandardResponseBody('Error', 'Number of week passes is a required field').to_dict()),400
     
    phone = request.form['phone']
    days = request.form['days']
    ends = request.form['ends']
    weeks = request.form['weeks']

    if 'name' in request.form:
        name = request.form['name'].split(' ')[0]
    else:
        name = ''

    return pass_controller.register_pass(user_data['user_id'],name,phone,days,ends,weeks)


def scan_pass(allowed_roles, is_only_for_admin):
    if 'token' not in request.headers:
        return jsonify(StandardResponseBody('Error', " 'token' is a required header").to_dict()),400
    
    token = request.headers['token']
    if not is_user_authenticated_and_authorized(token, allowed_roles, is_only_for_admin):
        return jsonify(StandardResponseBody('Error', 'User is not authorized to perform this operation').to_dict()), 401
    user_data = get_user_data(token)

    if 'code' not in request.form:
        return jsonify(StandardResponseBody('Error', " 'code' is a required field").to_dict()),400
    
    code = request.form['code']
        
    return pass_controller.scan_pass(user_data['user_id'], code)


def accept_pass(allowed_roles, is_only_for_admin):
    if 'token' not in request.headers:
        return jsonify(StandardResponseBody('Error', " 'token' is a required header").to_dict()),400
    
    token = request.headers['token']

    if not is_user_authenticated_and_authorized(token, allowed_roles, is_only_for_admin):
        return jsonify(StandardResponseBody('Error', 'User is not authorized to perform this operation').to_dict()), 401
    user_data = get_user_data(token)

    if 'type' not in request.form:
        return jsonify(StandardResponseBody('Error', " 'type' is a required field").to_dict()),400
    elif 'phone' not in request.form:
        return jsonify(StandardResponseBody('Error', " 'phone' is a required field").to_dict()),400
    elif 'qty' not in request.form:
        return jsonify(StandardResponseBody('Error', " 'quantity' is a required field").to_dict()),400
    
    type = request.form['type']
    phone = request.form['phone']
    qty = request.form['qty']

    return pass_controller.accept_pass(user_data['user_id'], type, phone, qty)


def get_qrs():
    if 'url' not in request.form:
        return jsonify(StandardResponseBody('Error'," 'url' is a required field").to_dict()),400
    
    url = request.form['url']
    
    return pass_controller.get_qrs(url)

def download_pass():
    if 'url' not in request.form:
        return jsonify(StandardResponseBody('Error'," 'url' is a required field").to_dict()),400
    
    url = request.form['url']

    return pass_controller.create_pass_for_customer(url)

def resend_url():
    if 'phone' not in request.form:
        return jsonify(StandardResponseBody('Error'," 'url' is a required field").to_dict()),400

    phone = request.form['phone']

    return pass_controller.resend_url(phone)

def delete_register(allowed_roles, is_only_for_admin):
    if 'token' not in request.headers:
        return jsonify(StandardResponseBody('Error', " 'token' is a required header").to_dict()),400
    
    token = request.headers['token']

    if not is_user_authenticated_and_authorized(token, allowed_roles, is_only_for_admin):
        return jsonify(StandardResponseBody('Error', 'User is not authorized to perform this operation').to_dict()), 401

    if 'id' not in request.form:
         return jsonify(StandardResponseBody('Error'," 'id' is a required field").to_dict()),400

    id = request.form['id']
    return pass_controller.delete_register(id)