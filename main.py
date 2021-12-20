
import WebServer
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        """Displays the content of the (templated) web site
            :param -
            :return: -
            """
        if self.path == '/':
            self.path = './html/index.html'
        else:
            self.path = './html' + self.path

        try:
            print(self.path[0:])
            file_to_open = open(self.path[0:]).read()
            self.send_response(200)
        except:
            file_to_open = "File Not Found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))
        return #BaseHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        """Handles post requests of a web client. Extracts key value pairs of the request (has to be extended)
            :param -
            :return: -
            """
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        self.keyvalue = dict(urllib.parse.parse_qsl(self.data_string))
        print(self.keyvalue[b'songname'])
        self.path = './html/profile.html'
        try:
            print(self.path[1:])
            file_to_open = open(self.path[2:]).read()
            song = self.keyvalue[b'songname'].decode('utf-8')
            file_to_open = file_to_open.replace('{favouritesong}', song)
            self.send_response(200)
        except:
            file_to_open = "File Not Found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

def StartupServer():
    """Starts the web server
        :param -
        :return: -
        """
    server = WebServer.HTTPWebServer()
    server.Initialize("localhost", 8080)
    server.Start(MyServer)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    """Entry point of the application
        :param -
        :return: -
        """
    StartupServer()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
