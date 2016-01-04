import BaseHTTPServer
import time
__author__ = 'Z500User'
HOST_NAME = 'localhost'
PORT_NUMBER = 8880

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        #global cp
        input_stream = open("cp.txt")
        cp = input_stream.readline()
        input_stream.close()
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<body>" + cp + "</body>")


    def do_POST(s):
        #global cp
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        cp = s.rfile.read()
        s.wfile.write("<body>" + cp + "</body>")
        output_stream = open("cp.txt", "w")
        output_stream.write(cp)
        output_stream.close()






if __name__ == '__main__':
    #cp = ""
    print 'Old, obsolete file version. Try using sync/server.py instead'
    raise SystemError('obsolete version')
    output_stream = open("cp.txt", "w")
    output_stream.write("not init yet")
    output_stream.close()
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), ' server starting'
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), ' server closing'
