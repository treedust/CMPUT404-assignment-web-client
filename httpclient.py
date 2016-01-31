#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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
        host = ""
        port = 80
        tmpurl = url
        try:
            re.search('^HTTP://|http://',tmpurl).group(0)
        except:
            tmpurl ='HTTP://'+tmpurl        
        hostport1 = re.search('(?<=(HTTP://|http://)).*(?<=[:\d+])',tmpurl)
        try:
            host = hostport1.group(0).split(":")[0]
            port = hostport1.group(0).split(":")[1]
            if port == '':
                host += ":" 
                port = 80
            if "/" in port:
                port = port.split("/")[0]
            return [host,port]
        except:
            #no port found 
            #split on /
            host = tmpurl.split("/")[2]
        try:
            path = "/"
            for i in tmpurl.split("/")[3:]:
                if i == '':
                    path += i
            return [host,port,path]
        except:
        	pass
        return [host,port,"/"]

    def connect(self, host, port):
        # use sockets
        mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mysocket.connect((host,port))
        return mysocket 

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
        hp = self.get_host_port(url)
        s = self.connect(hp[0],int(hp[1]))
        s.sendall("GET / HTTP/1.1\nHost: "+str(hp[0])+"\r\n\r\n")
        response = self.recvall(s)
        print (response)
        sys.stdout.flush()
        a = re.search('^HTTP/1\..*',response)
        try:
        	HTTPcodemsg = a.group(0)
        	code = HTTPcodemsg.split(" ")[1]
        except:
        	pass
        #get body 
        try:
        	body = re.search('<(HTML|html)>[\S\s]*',response).group(0)
        except:
        	body = ""
        print ("Code: " + str(code))
        print (body)
        sys.stdout.flush()
        return HTTPResponse(int(code), body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )   
