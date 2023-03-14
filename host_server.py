import pub_sub as psb

import http.server
import socketserver
from urllib.parse import parse_qs
import os

PORT = 8000

class handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        print("GET REQUEST")
        referer = self.headers.get('Referer')
        self.protocol_version='HTTP/1.1'
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        with open("index.html", 'r') as file:
            self.wfile.write(bytes(file.read(), 'UTF-8'))
    
    def do_POST(self):
        print("POST REQUEST")
        length = int(self.headers['content-length'])
        postvars = parse_qs(
                self.rfile.read(length), 
                keep_blank_values=1)
        print(postvars)

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
    os.system("ipconfig")
    print("serving at port", PORT)
    httpd.serve_forever()






def generate_publishers():
    PUBLISHERS = 3
    with open("channels.txt", 'r') as file:
        for n in range(PUBLISHERS):
            Id   = file.readline().strip()
            name = file.readline().strip()
            desc = file.readline().strip()
            psb.create_publisher(Id, name, desc)
            file.readline().strip()


if __name__ == "__main__":
    generate_publishers()
