#! /usr/bin/python3

import json
import socket
import requests

from bs4 import BeautifulSoup

class TCPDaemon(object):
    def __init__(self):
        self.sock = socket.socket()
        self.sock.bind(('', 9090))
        self.sock.listen(1)

    def get_message(self, sock):
        result = b''
        while True:
            data = sock.recv(1024)
            if not data:
                break
            result += data
        return result

    def get_url_info(self, url):
        print('Incoming url: {}'.format(url))
        response = requests.get(url.strip())
        soup = BeautifulSoup(response.text, 'lxml')
        d = {}
        d['title'] = soup.find("meta",  property="og:title")['content']
        d['desc'] = soup.find("meta",  property="og:description")['content']
        d['image'] = soup.find("meta",  property="og:image")['content']
        return json.dumps(d)

    def loop_forever(self):
        while True:
            sock, addr = self.sock.accept()
            print("Get message...")
            result = self.get_message(sock)
            info = self.get_url_info(result)
            print("End get message...")
            sock.send(info.encode('utf8'))
            sock.close()

if __name__ == "__main__":
    daemon = TCPDaemon()
    daemon.loop_forever()
