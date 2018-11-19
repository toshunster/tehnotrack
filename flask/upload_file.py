#! /usr/bin/env python3

import sys
import base64
from jsonrpc.proxy import ServiceProxy

if __name__ == "__main__":
    if len( sys.argv ) != 2:
        print( "Usage: {} filename".format( sys.argv[0] ) )
        sys.exit(1)
    filename = sys.argv[1]
    service = ServiceProxy( 'http://127.0.0.1:5000/api/' )
    with open( filename, 'rb' ) as input_file:
        content = input_file.read()
        b64_content = base64.b64encode( content ).decode('utf8')
        print( b64_content )

        #response = service.api.upload_file( b64_content, filename )
        #print( "Response: {}".format( response ) )
        response = service.api.download_file( filename )
        print( "Response: {}".format( response ) )
        #content = base64.b64decode( b64_content ).decode('utf8')
        #print( content )