#!/usr/bin/env python

import time
import BaseHTTPServer
import os


HOST_NAME = 'localhost'
PORT_NUMBER = 8802
my_dict = dict()


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def log(self, text):
        print text

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        global files_info
        global my_dict
        req_path = s.path
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><body>")
        s.wfile.write(my_dict[req_path])
        s.wfile.write("</body></html>")

    def do_POST(s):
        global files_info
        global my_dict
        req_path = s.path
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        files_info = s.rfile.read()
        my_dict[req_path] = files_info
        s.wfile.write("<html><body>" + files_info + "</body></html>")

    def do_UPLOAD(s):
        '''
        file transfer from client to server
        '''
        upload_path, upload_filename = os.path.split(os.path.abspath(s.path.lstrip('/')))
        try:
            os.makedirs(upload_path)
        except os.error, e:
            s.log('directory exists or cannot be created')
            #s.send_response(400)
            #s.end_headers()
            #return
        output_stream = open(os.path.join(upload_path, upload_filename), "w")
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

        file_data_len = s.headers.getheader('content-length')
        file_data_len = 0 if file_data_len == None else int(file_data_len)

        file_data = s.rfile.read(file_data_len)
        output_stream.write(file_data)
        s.wfile.write("<html><body> got " + os.path.join(upload_path, upload_filename) + "</body></html>")
        output_stream.close()

    def do_DOWNLOAD(s):
        '''
        File transfer from server to client
        '''
        download_path, download_filename = os.path.split(os.path.abspath(s.path.lstrip('/')))
        try:
            input_stream = open(os.path.join(download_path, download_filename))
        except:
            input_stream = None
        if input_stream is None:
            s.sent_response(404)
            s.end_headers()
            s.wfile.write(os.path.join(download_path, download_filename) + ' not found')
            return

        file_data = ''
        while True:
            line = input_stream.readline()
            if line == '':
                break
            file_data += line
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.send_header("content-length", str(len(file_data)))
        s.end_headers()

        s.wfile.write(file_data)
        input_stream.close()


if __name__ == '__main__':
    files_info = "AAAA"
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
