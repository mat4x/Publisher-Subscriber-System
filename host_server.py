import pub_sub as psb

import http.server
import socketserver
from urllib.parse import parse_qs
import os

PORT = 8000

class handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = r'./index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        print("POST REQUEST")
        length = int(self.headers['content-length'])
        postvars = parse_qs(
                self.rfile.read(length), 
                keep_blank_values=1)
        print(postvars)

Handler = http.server.SimpleHTTPRequestHandler



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
    
    with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
        os.system("ipconfig")
        print("serving at port", PORT)
        httpd.serve_forever()
