from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

## import CRUD Operations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurant"):
                result = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                for restaurant in result:
                    output += restaurant.name
                    output += "</br>"
                self.wfile.write(output)
                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>Hello!"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
                output += "<h2> What would you like me to say? </h2>"
                output += "<input name='message' type='text'>"
                output += "<input type='submit' value='Submit'></form>"
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
            if ctype == 'multipart/form-data':
                fields=cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

                output = ""
                output += "<html><body>"
                output += "<h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]

                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
                output += "<h2> What would you like me to say? </h2>"
                output += "<input name='message' type='text'>"
                output += "<input type='submit' value='Submit'></form>"

                output += "</body></html>"
                self.wfile.write(output)
                print output

        except:
            pass

def main():
    try:
        port = 3653
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()