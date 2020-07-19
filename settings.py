from flask_cors import CORS
from flask import Flask


app = Flask(__name__)
cors = CORS(app, allow_headers="token", expose_headers="token")

environment = 'prod' # dev or stag or prod

username = 'oyw_' + environment
password = 'oyw_19_' + environment
database = 'oyw_' + environment

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+ username +':' + password + '@127.0.0.1/' + database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'blahhhh'
app.config['JWT_ALGORITHM'] = 'HS256'
app.config['TEXT_LOCAL_API_KEY'] = 'messaging_key'
app.config['DATE_FASHION_SHOW'] = 6
