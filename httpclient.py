#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
        parts  = url.split(':')
        address = ""
        port    = ""
        path    = ""
        if (parts[0] == 'http'):
            if len(parts) > 2:
                #got a port
                portNpath = parts[2].split('/')
                port = portNpath[0]
                try:
                    int(port)
                    for i in portNpath[1:-1]:
                        path += i
                        path += '/'
                    path += portNpath[-1]
                except:
                    for i in portNpath[1:-1]:
                        path += i
                        path += '/'
                    if portNpath[-1] == '':
                        path += '/'
                    else:
                        path += portNpath[-1]
                    port = 80 
                address = parts[1]
            else:
                #port is 80 
                port = 80
                getPath = parts[1].split('/')
                address = '//'+getPath[2]
                for i in getPath[1:-1]:
                    path += i
                    path += '/'
                if getPath[-1] == '':
                    path += '/'
                else:
                    path += getPath[-1]
        else:
            self.get_host_port("http://"+url)
        # [http: , //address, path, to, dst ], port 
        return address[2:], path, port 

    def connect(self, host, port):
        # use sockets!
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((host, port))
        return None

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        code = 500
        body = ""
        host, path, port =  self.get_host_port(url)
        try:
            self.connect(host, int(port) ) 
        except:
            #error connecting to host 
            return HTTPResponse(code, body)
        request = "GET / HTTP/1.0\n\n"
        self.clientSocket.sendall(request)
        print ('Host is: ', host) 
        print (self.recvall(self.clientSocket))
        sys.stdout.flush()
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        host, path, port =  self.get_host_port(url)
        try:
            self.connect(host+"/", int(port) ) 
        except:
            #error connecting to host 
            return HTTPResponse(code, body)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    #client.connect("www.mcmillan-inc.com",80)
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )
