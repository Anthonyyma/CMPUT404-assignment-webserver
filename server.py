#  coding: utf-8 
import socketserver
import mimetypes

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#

# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

#https://www.codementor.io/@joaojonesventura/building-a-basic-http-server-from-scratch-in-python-1cedkg0842

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)

        headers = self.data.split(b'\n')
        method = headers[0].split()[0]
        filename = headers[0].split()[1]

        method = method.decode("utf-8")
        filename = filename.decode("utf-8")

        if method == "PUT" and filename[-3:] == "css":
            response = "HTTP/1.0 405 NOT FOUND\r\nFile Not Found"
        else:
            if filename[-1] == "/":
                filename += "index.html"
            try:
                f = open("www" + filename)
                data = f.read()
                mimeString = mimetypes.guess_type("www" + filename)
                f.close()
                response = "HTTP/1.1 200 OK\r\n" + "Host: 127.0.0.1:8080\r\nContent-Type: " + mimeString[0] + "\r\n\r\n" + data

            except:
                response = "HTTP/1.0 404 NOT FOUND\r\nFile Not Found"

        self.request.sendall(response.encode())

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
