from flask import Flask

from flask_jsonrpc import JSONRPC

import boto3
import config

#from authlib.flask.client import OAuth
from flask_oauth import OAuth


app = Flask(__name__)
app.secret_key = 'adfasjfh23437fhufhskjfd'
#oauth = OAuth(app)

#oauth.init_app( app )

jsonrpc = JSONRPC( app, '/api/' )

s3_session = boto3.session.Session()
s3_client = s3_session.client( service_name='s3',\
                               endpoint_url=config.S3_ENDPOINT_URL,\
                               aws_access_key_id=config.S3_ACCESS_KEY_ID,\
                               aws_secret_access_key=config.S3_SECRET_ACCESS_KEY  )

oauth = OAuth()

vk = oauth.remote_app('vk',
    base_url='https://api.vk.com/method/',
    request_token_url=None,
    access_token_url='https://oauth.vk.com/access_token',
    authorize_url='https://oauth.vk.com/authorize',
    consumer_key=config.VK_APP_ID,
    consumer_secret=config.VK_APP_SECRET,
    request_token_params={'scope': 'email'})


from .views import *
