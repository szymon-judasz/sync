from urlparse import urlparse
import httplib
__author__ = 'Z500User'


class FileTransmitter():
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def upload_file_to_server(self, remote_file_path, local_file_path):
        input_stream = open(local_file_path)
        file_data = ''
        while True:
            line = input_stream.readline()
            if line == '':
                break
            file_data += line
        input_stream.close()

        request_url = 'http://' + self.address + ':' + self.port + '/' + remote_file_path
        parsed_url = urlparse(request_url)
        fact = httplib.HTTPConnection
        conn = fact(parsed_url.netloc)
        conn.request('UPLOAD', parsed_url.path, file_data)
        conn.getresponse()

    def download_file_from_server(self, remote_file_path, local_file_path):
        request_url = 'http://' + self.address + ':' + self.port + '/' + remote_file_path
        parsed_url = urlparse(request_url)
        fact = httplib.HTTPConnection
        conn = fact(parsed_url.netloc)
        conn.request('DOWNLOAD', parsed_url.path)

        resp = conn.getresponse()
        response_size = resp.getheader('content-length')
        response_data = resp.read(response_size)

        output_stream = open(local_file_path, 'w')
        output_stream.write(response_data)
        output_stream.close()
        resp.close()
        conn.close()

if __name__ == "__main__":
    ft = FileTransmitter('127.0.0.1', '8802')
    ft.download_file_from_server('uploadtest.txt', 'downloadtest.txt')
