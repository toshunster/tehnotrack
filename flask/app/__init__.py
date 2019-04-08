from flask import Flask

from flask_jsonrpc import JSONRPC

import boto3
import settings

#from authlib.flask.client import OAuth
from flask_oauth import OAuth

from flask_cache import Cache

#from werkzeug.contrib.profiler import ProfilerMiddleware

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'adfasjfh23437fhufhskjfd'

app.config.from_object('instance.config.ProductionConfig')

#app.config.from_object('instance.config.DevelopmentConfig')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://quack@localhost/quack_new'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://quack:4NMIIJvl1r@89.208.86.185/quack'

db = SQLAlchemy( app )

cache = Cache( app,config={'CACHE_TYPE': 'simple'})

#oauth = OAuth(app)

#oauth.init_app( app )

jsonrpc = JSONRPC( app, '/api/' )

s3_session = boto3.session.Session()
s3_client = s3_session.client( service_name='s3',\
                               endpoint_url=settings.S3_ENDPOINT_URL,\
                               aws_access_key_id=settings.S3_ACCESS_KEY_ID,\
                               aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY  )

oauth = OAuth()

vk = oauth.remote_app('vk',
    base_url='https://api.vk.com/method/',
    request_token_url=None,
    access_token_url='https://oauth.vk.com/access_token',
    authorize_url='https://oauth.vk.com/authorize',
    consumer_key=settings.VK_APP_ID,
    consumer_secret=settings.VK_APP_SECRET,
    request_token_params={'scope': 'email'})


from .views import *
from .models import *
