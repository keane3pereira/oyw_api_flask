from helpers.auth_helper import get_user_data, is_user_authenticated_and_authorized
from controllers import volunteer_controller
from responses import StandardResponseBody
from flask import request, jsonify


role_map = {'sa':['sa','as','ar','r','s'],
            'ar':['r'],
            'as':['s']
            }


def get_all_volunteers(allowed_roles, is_only_for_admin):
    if 'token' not in request.headers:
        return jsonify(StandardResponseBody('Error', 'Token is a required field').to_dict()), 400

    token = request.headers['token']
    if not is_user_authenticated_and_authorized(token, allowed_roles, is_only_for_admin):
        return jsonify(StandardResponseBody('Error', 'User is not authorized to perform this operation').to_dict()), 401

    user_data = get_user_data(token)
    
    return volunteer_controller.get_all_volunteers(user_data)


def set_volunteer_status(allowed_roles, is_only_for_admin, vid):
    if 'token' not in request.headers:
        return jsonify(StandardResponseBody('Error', 'Token is a required field').to_dict()), 400

    token = request.headers['token']
    if not is_user_authenticated_and_authorized(token, allowed_roles, is_only_for_admin):
        return jsonify(StandardResponseBody('Error', 'User is not authorized to perform this operation').to_dict()), 401
    user_data = get_user_data(token)

    if 'is_active' not in request.form:
        return jsonify(StandardResponseBody('Error', '"is_active" is a required field').to_dict()), 400

    is_active = request.form['is_active'] == 'true'
    
    return volunteer_controller.set_volunteer_status(user_data, vid, is_active)


def create_volunteer(allowed_roles, is_only_for_admin):
    if 'token' not in request.headers:
        return jsonify(StandardResponseBody('Error', 'Token is a required field').to_dict()), 400

    token = request.headers['token']
    if not is_user_authenticated_and_authorized(token, allowed_roles, is_only_for_admin):
        return jsonify(StandardResponseBody('Error', 'User is not authorized to perform this operation').to_dict()), 401
    user_data = get_user_data(token); #print(user_data)

    if user_data['role'] == 'sa' and 'role' not in request.form:
        return jsonify(StandardResponseBody('Error', "'role' is a required field").to_dict()), 400
    elif 'name' not in request.form:
        return jsonify(StandardResponseBody('Error', "'name' is a required field").to_dict()), 400
    elif 'username' not in request.form:
        return jsonify(StandardResponseBody('Error', "'username' is a required field").to_dict()), 400
    elif 'password' not in request.form:
        return jsonify(StandardResponseBody('Error', "'password' is a required field").to_dict()), 400
    elif 'is_active' not in request.form:
        return jsonify(StandardResponseBody('Error', "'is_active' is a required field").to_dict()), 400
    
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    is_active = bool(request.form['is_active'])
    role = request.form['role']

    if role not in role_map[user_data['role']]:
        #print(role_map[user_data['role']])
        return jsonify(StandardResponseBody('Error', " Invalid role entered for user ").to_dict()), 400

    return volunteer_controller.create_volunteer(user_data['user_id'], name, username, password, is_active, role)