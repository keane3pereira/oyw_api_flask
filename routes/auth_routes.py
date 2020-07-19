from flask import Flask, request, Response, jsonify
from responses import StandardResponseBody
from controllers import auth_controller


def login():
    if 'username' not in request.form:
        return jsonify(StandardResponseBody('Error', 'Username is a required field').to_dict()),400
    elif 'password' not in request.form:
        return jsonify(StandardResponseBody('Error', 'Password is a required field').to_dict()),400
    
    username = request.form['username']
    password = request.form['password']
    
    return auth_controller.login(username, password)
