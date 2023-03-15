import pub_sub as psb

import http.server
import socketserver
from urllib.parse import parse_qs
import os

PORT = 8000

class handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self, path="index.html"):
        # Cache request
        path = self.path

        # Validate request path, and set type
        if ".html" in path:
            type = "text/html"
        elif path == "/script.js":
            type = "text/javascript"
        elif path == "/style.css":
            type = "text/css"
        elif path == "/favicon.ico":
            type = "image/x-icon"
        else:
            # Wild-card/default
            if not path == "/":
                print("UNRECONGIZED REQUEST: ", path)
                
            path = "/index.html"
            type = "text/html"
        
        # Set header with content type
        self.send_response(200)
        self.send_header("Content-type", type)
        self.end_headers()
        
        # Open the file, read bytes, serve
        print("-------------", path)
        with open(path[1:], 'rb') as file:
            if path not in ("/index.html", "/notification.html"):
                self.wfile.write(file.read()) # Direct Send
            else:
                html = file.read().decode('utf-8')
                result = self.dynamic_inject(html, path) #HTML INJECTION
                print(result)
                self.wfile.write(result.encode('utf-8'))

    
    def do_POST(self):
        print("POST REQUEST")
        length = int(self.headers['content-length'])
        postvars = parse_qs(
                self.rfile.read(length), 
                keep_blank_values=1)

        postvar = dict()
        for key in postvars.keys():
            postvar[key.decode()] = postvars[key][0].decode()

        do_action(postvar)

    def dynamic_inject(self, html, path):
        print("INJECT", path)
        if path == "/index.html":
            template = '''
<div class="channel">
    <div class="photo"></div>
        <div class="details">
            <h2>{pblshr.name}</h2>
	    <p>{pblshr.description}</p>
		</div>
		<button value="slyplt">Subscribe</button>
	</div>'''
            sections = html.split("<!-- SPLIT -->")
            for publisher in psb.PUBLISHERS.values():
                sections.insert( -1, template.format(pblshr=publisher) )

            print(sections)
            return ''.join(sections)

        elif path == "/notification.html":
            return html

        else:
            print("WHAT")
            return html
            
            
        

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


def do_action(arguments):
    print(arguments)
    action = arguments['action']
    
    if action == "publish":
        publisher_name = arguments['publisher']
        try:
            publisher_obj = psb.PUBLISHERS[publisher_name]
            publisher_obj.publish_message(arguments['content'])
        except:
            print("Publisher not found")
        
        
    
if __name__ == "__main__":
    generate_publishers()
    
    with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
        os.system("ipconfig")
        print("serving at port", PORT)
        httpd.serve_forever()
