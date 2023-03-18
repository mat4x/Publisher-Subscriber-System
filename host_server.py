import pub_sub as psb

import http.server
import socketserver
from urllib.parse import parse_qs
import os
import datetime

PORT = 8000

class handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self, path="index.html"):
        # Cache request
        path = self.path
        #print("#"*20, path)

        # Validate request path, and set type
        if ".html" in path:
            req_type = "text/html"
        elif ".js" in path:
            req_type = "text/javascript"
        elif path == "/style.css":
            req_type = "text/css"
        elif path == "/favicon.ico":
            req_type = "image/x-icon"
        elif ".jpg" in path:
            req_type = "image/x-icon"
        else:
            # Wild-card/default
            if not path == "/":
                print("UNRECONGIZED REQUEST: ", path)
                
            path = "/index.html"
            req_type = "text/html"
        
        # Set header with content type
        self.send_response(200)
        self.send_header("Content-type", req_type)
        self.end_headers()
        
        # Open the file, read bytes, serve
        with open(path[1:], 'rb') as file:
            if path not in ("/index.html", "/notification.html"):
                self.wfile.write(file.read()) # Direct Send
            else:
                html = file.read().decode('utf-8')
                result = self.dynamic_inject(html, path, self.client_address[0]) #HTML INJECTION
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

        do_action(postvar, self.client_address[0])
        self.send_response(200)

    def dynamic_inject(self, html, path, cltIP):
        print("INJECT", path)
        if path == "/index.html":
            template = TEMPLATES["channels"]
            sections = html.split("<!-- SPLIT -->")

            for publisher in psb.PUBLISHERS.values():
                sections.insert( -1, template.format(pblshr=publisher) )
            return ''.join(sections)

        elif path == "/notification.html":
            for sub in psb.SUBSCRIBERS.values():
                if sub.IP == cltIP:
                    subscriber = sub
                    break
    
            notifications = list()

            for pblshr in subscriber.subscriptions:
                with open(f"{pblshr.Id}.csv") as database:
                    content = 1
                    while True:
                        content = database.readline().strip().split(',')
                        if content == ['']: break
                        notifications.append(content + [pblshr.name])
            
            notifications.sort(key=lambda x: -float(x[0]))

            sections = html.split("<!-- SPLIT -->")
            template = TEMPLATES["notifications"]

            for notif in notifications:
                dt_obj = datetime.datetime.fromtimestamp( float(notif[0]) )
                date = f"{dt_obj.day}-{dt_obj.month}-{dt_obj.year}"
                sections.insert( -1, template.format(
                    channel_name = notif[2],
                    date = date,
                    message = notif[1]) )
            count = subscriber.unread
            subscriber.unread = 0
            return ''.join(sections).format(unread_count=count)

        else:
            print('#'*10, "WHAT")
            return html
            
            
        


def generate_publishers():
    with open("channels.txt", 'r') as file:
        while True:
            Id   = file.readline().strip()
            if Id == '': break
            name = file.readline().strip()
            desc = file.readline().strip()
            img_link = file.readline().strip()
            psb.create_publisher(Id, name, desc, img_link)
            file.readline().strip()


def do_action(arguments, client_adr=None):
    print(arguments)
    action = arguments['action']
    
    if action == "publish":
        publisher_usr_name = arguments['publisher']
        try:
            publisher_obj = psb.PUBLISHERS[publisher_usr_name]
            publisher_obj.publish_message( arguments['content'] )
        except:
            print("Publisher not found")

    elif action == "sub_login":
        subscriber_usr_name = arguments['subscriber']
        if subscriber_usr_name not in psb.SUBSCRIBERS:
            psb.create_subscriber(subscriber_usr_name, client_adr)
        else:
            psb.SUBSCRIBERS[subscriber_usr_name].IP = client_adr
            print(f"Welcome back {subscriber_usr_name}")

    elif action == "subscribe":
        psb.SUBSCRIBERS[ arguments['sub'] ].subscribe( psb.PUBLISHERS[ arguments['channel'] ] )

##        for pubs in psb.PUBLISHERS.values():
##            print(pubs.subscribers)
##        for subs in psb.SUBSCRIBERS.values():
##            print(subs.subscriptions)
        
        
        
        
TEMPLATES = {
    "channels" : '''<div class="channel">
    <img src="{pblshr.img_lnk}" class="photo" onerror="this.onerror=null; this.src='Default.jpg'" alt="{pblshr.name}_img">
        <div class="details">
            <h2>{pblshr.name}</h2>
	    <p>{pblshr.description}</p>
		</div>
		<button id="{pblshr.Id}_btn" value="{pblshr.Id}" onclick="subscribe('{pblshr.Id}');">Subscribe</button>
	</div>''',

    "notifications" : '''<div class="message">
      <h2>{channel_name}</h2>
      <p>{date}</p>
      <p>{message}</p>
    </div>'''
    }


if __name__ == "__main__":
    generate_publishers()
    
    with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
        os.system("ipconfig")
        print("serving at port", PORT)
        httpd.serve_forever()
