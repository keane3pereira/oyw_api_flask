from settings import *
import requests


def send_transactional_sms(numbers, message):
    
    sender = 'OYWOYA'
    apikey = app.config['TEXT_LOCAL_API_KEY']

    # api-endpoint
    URL = "https://api.textlocal.in/send"

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'apikey': apikey, 'numbers': numbers,
              'message': message, 'sender': sender}
    # sending get request and saving the response as response object
    response = requests.get(url=URL, params=PARAMS)

    # extracting data in json format
    data = response.json()
    return data
