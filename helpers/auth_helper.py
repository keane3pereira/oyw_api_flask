from jwt import encode, decode
from models import Volunteer
from settings import *


temp_tokens = { }

def is_user_authenticated_and_authorized(token, allowed_roles, is_only_for_admin):
    
    allowed_roles = ['sa'] + allowed_roles

    if token in temp_tokens:
        user_data = temp_tokens[token]
    else:
        user_data = decode(token, app.config['JWT_SECRET_KEY'], algorithm=app.config['JWT_ALGORITHM'])
        temp_tokens[token] = user_data
    #print(user_data, allowed_roles)
    
    if user_data['is_admin'] == False and is_only_for_admin == True:
        return False
    elif len(allowed_roles) !=1 and user_data['role'] not in allowed_roles:
        return False

    volunteer = Volunteer.find_by_id(user_data['user_id'])
    if volunteer == None:
        return False

    return True

def get_user_data(token):

    if token in temp_tokens:
        return temp_tokens[token]

    user_data = decode(token, app.config['JWT_SECRET_KEY'], algorithm=app.config['JWT_ALGORITHM'])
    temp_tokens[token] = user_data

    return user_data

def reset_temp_tokens():
    global temp_tokens
    temp_tokens = {}