from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from io import BytesIO

class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "<h1>Hello!</h1>"
            message += '''<form method='POST' enctype='multipart/form-data' action = '/hello'><h2> What would you like me to say</h2><input name='message' type ='text'><input type = 'submit' value= 'Submit'></form>'''
            message += "</body></html>"
            self.wfile.write(message)
            print message
            return

        if self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "<h1>&#161Hola!</body></h1>"
            message += '''<form method='POST' enctype='multipart/form-data' action = '/hola'><h2> What would you like me to say</h2><input name='message' type ='text'><input type = 'submit' value= 'Submit'></form>'''
            message +="</body></html>"
            self.wfile.write(message)
            print message
            return
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        ctype, pdict = cgi.parse_header(self.headers.get('Content-type'))
        # pdict['boundary'] = bytes(pdict['boundary'],"utf-8")
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            messagecontent = fields.get('message')
        output = ""
        output += "<html><body>"
        output += "<h2>How about this?</h2>"
        output += "<h1>"
        # self.wfile.write(bytes(output, "UTF-8"))
        self.wfile.write(messagecontent[0])
        output = ""
        output += "</h1>"
        output +='''<form method='POST' enctype='multipart/form-data' action = '/hola'><h2> What would you like me to say</h2><input name='message' type ='text'><input type = 'submit' value= 'Submit'></form>'''
        output += "</body></html>"
        self.wfile.write(output.encode('utf-8'))
        print (output)
        return

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
