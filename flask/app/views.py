from flask import request, abort, jsonify,redirect, url_for, session
import json
import base64
import settings
import time

import hmac
import hashlib

from app import app, jsonrpc, s3_client, vk, cache, db

from flask import make_response

from .models import Person
import random

import socket

@cache.memoize()
def get_random( num ):
    print( "get_random" )
    time.sleep(2)
    return random.randint(0, num)

@app.route('/test/<string:name>/')
@app.route('/test/')
def index_test(name="world"):
    return "Hello, {}! Random: {} / {}".format( name, get_random( 10 ), get_random(1000) )

@app.route('/url_viewer/')
def url_viewer():
    urls = ['https://mail.ru', 'https://ya.ru' ]#, 'https://google.com']
    url = random.choice(urls)
    sock = socket.socket()
    #sock.timeout(5)
    sock.connect(('127.0.0.1', 9090))
    print("Sending url: {}".format(url))
    sock.send(url.encode('utf8'))
    result = b''
    while True:
        data = sock.recv(1024)
        if not data:
            break
        result += data
    sock.close()
    return jsonify(result.decode('utf8'))

@app.route('/create/<string:name>/')
def create_user(name):
    first_name = random.choice([ "Tom", "Jerry", "Mike"])
    person = Person(name, first_name)
    db.session.add(person)
    db.session.commit()
    return first_name

def jsonify_person(person):
    result = {}
    result['id'] = person.id
    result['first_name'] = person.first_name
    result['nickname'] = person.username
    return result

@app.route('/view/')
def view_user():
    persons = Person.query.all()
    return jsonify([jsonify_person(person) for person in persons])

@app.route('/form/', methods=['GET', 'POST'])
def form():
    if request.method == "GET":
        return """<html><head></head><body>
        <form method="POST" action="/form/">
            <input name="first_name" >
            <input name="last_name" >
            <input type="submit">
        </form>
        </body></html>"""
    else:
        rv = jsonify( request.form )
        return rv

@jsonrpc.method( 'print_name' )
def foo():
    return { "name": "Ivan" }

@jsonrpc.method( 'api.upload_file' )
def upload_file( b64content, filename ):
    content = base64.b64decode( b64content ).decode( 'utf-8' )
    s3_client.put_object( Bucket=settings.S3_BUCKET_NAME, Key=filename, Body=content )
    return b64content

@jsonrpc.method( 'api.download_file' )
def download_file( filename ):
    response = s3_client.get_object( Bucket=settings.S3_BUCKET_NAME, Key=filename )
    content = response.get('Body').read().decode('utf8')
    print( content, dir( response ) )
    return content

def generate_key( key, message ):
    key = bytes(key, 'UTF-8')
    message = bytes(message, 'UTF-8')
    
    digester = hmac.new(key, message, hashlib.sha1)
    #signature1 = digester.hexdigest()
    signature1 = digester.digest()
    return base64.b64encode( signature1 )

@app.route( '/api/file/<string:filename>' )
def get_file( filename ):
    response = make_response()
    #response.mimetype = "image/jpeg"
    
    #Thu, 18-Nov-10 11:27:35 GMT
    now = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime() )
    string_to_sign = "GET\n\n\n\nx-amz-date:{}\n/{}/{}".format( now, settings.S3_BUCKET_NAME, filename )
    signature = generate_key( settings.S3_SECRET_ACCESS_KEY, string_to_sign ).decode( 'utf8' )
    print( "String to sign: [{}], signature: [{}]".format( string_to_sign, \
                                                           signature ) )
    response.headers['Authorization'] = "AWS {}:{}".format( settings.S3_ACCESS_KEY_ID, signature  )
    response.headers['X-Amz-Date'] = now
    response.headers['Date'] = now
    response.headers['Host'] = "{}.hb.bizmrg.com".format( settings.S3_BUCKET_NAME )
    response.headers['X-Accel-Redirect'] = "/s3/{}".format( filename )
    print( response.headers )
    return response

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return vk.authorize(callback=url_for('vk_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/login/authorized')
@vk.authorized_handler
def vk_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    access_token = resp['access_token']
    email = resp.get('email')
    session['oauth_token'] = (resp['access_token'], '')
    return "Email: {}".format( email )

@vk.tokengetter
def get_vk_oauth_token():
    return session.get('oauth_token')


