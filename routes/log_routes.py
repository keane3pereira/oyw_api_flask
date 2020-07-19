from helpers.auth_helper import is_user_authenticated_and_authorized, get_user_data
import controllers.auth_controller as auth_controller
from flask import Flask, request, Response, jsonify
import controllers.log_controller as log_controller
from responses import StandardResponseBody


def get_all_customer_transactions(allowed_roles, is_only_for_admin):
    if 'token' not in request.headers:
        return jsonify(StandardResponseBody('Error', "'token' is a required field").to_dict()),400

    token = request.headers['token']
    if not is_user_authenticated_and_authorized(token, allowed_roles, is_only_for_admin):
        return jsonify(StandardResponseBody('Error', 'User is not authorized to perform this operation').to_dict()), 401

    if 'phone' not in request.form:
        return jsonify(StandardResponseBody('Error', "'phone' is a required field").to_dict()),400

    phone = request.form['phone']
       
    return log_controller.get_details_by_phone(phone)


def get_all_logs(allowed_roles, is_only_for_admin):
    return log_controller.get_all_logs()

    
def create_passes_excel(allowed_roles, is_only_for_admin):
    if 'token' not in request.headers:
            return jsonify(StandardResponseBody('Error', "'token' is a required field").to_dict()),400
    
    token = request.headers['token']
    if not is_user_authenticated_and_authorized(token, allowed_roles, is_only_for_admin):
        return jsonify(StandardResponseBody('Error', 'User is not authorized to perform this operation').to_dict()), 401

    return log_controller.create_excel_for_passes()