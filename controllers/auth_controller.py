from responses import StandardResponseBody, LoginResponseBody
from flask import Response, jsonify
from models import Volunteer
from settings import app
from jwt import encode


def login(username, password):
    admin = Volunteer.find_by_username_and_role(username, ['sa','as','ar'])
    volunteer = Volunteer.find_by_username(username)

    user = admin if admin != None else volunteer
    #print(admin, volunteer, user)

    if user == None:
        return jsonify(StandardResponseBody('Error', 'Username does not exist').to_dict()), 400
    elif user.password != password:
        return jsonify(StandardResponseBody('Error', 'Password is incorrect').to_dict()), 400
    
    token_data = {
        'role': user.role, 
        'user_id': admin.vid if admin != None else volunteer.vid
        }

    if admin != None:
        token_data['is_admin'] = True
    elif volunteer != None:
        token_data['is_admin'] = False
    #print(token_data)

    jwt_token = encode(token_data, app.config['JWT_SECRET_KEY'], algorithm=app.config['JWT_ALGORITHM'])

    user_to_return = {
        'name': user.name,
        'role': user.role,
        'is_admin': token_data['is_admin']
        }
    
    response = jsonify(LoginResponseBody('Success', 'Successfully logged in user', dict(user_to_return)).to_dict())
    response.headers['token'] = jwt_token
    return response