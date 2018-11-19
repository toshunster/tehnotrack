import unittest
import json

from app import app

class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_index(self):
        rv = self.app.get('/test/')
        self.assertEqual( 200, rv.status_code )
        self.assertEqual( b'Hello, world!', rv.data )
        self.assertEqual( "text/html", rv.mimetype )
        pass

    def test_form(self):
        rv = self.app.post('/form/', data={ 'first_name': "Jesse",\
                                            'last_name': "Pinkman" })
        expected_response = {"first_name":"Jesse","last_name":"Pinkman"}
        self.assertEqual( expected_response, json.loads( rv.data ) )

    def tearDown(self):
        pass

class JSONRPCTest( unittest.TestCase ):
    def setUp(self):
        self.app = app.test_client()
    
    def test_print_name(self):
        # Аналог команды curl.
        # curl -i -X POST -H "Content-type: application/json" --data @request.json 
        # http://127.0.0.1:5000/api/
        #rv = self.app.post('/api/', data='{ "jsonrpc": "2.0", "method": \
        #                            "print_name", "params": [], "id": 1 }', \
        #                            content_type='application/json')
        params = { "name" : "Jack", "last_name": "Welker" }
        rpc_query = { "jsonrpc": "2.0", "method": "print_name", \
                      "params": params, "id": 1 }
        rpc_expected = { "id":1, "jsonrpc":"2.0", "result":{"name":"Jack"} }
        rv = self.app.post('/api/', data=json.dumps( rpc_query ), \
                                    content_type='application/json')
        self.assertEqual( rpc_expected, json.loads( rv.data ) )


if __name__ == "__main__":
    unittest.main()
