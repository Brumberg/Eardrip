
import python.webserver
from http.server import BaseHTTPRequestHandler
import urllib.parse
from python.rema import remotedatabase as rema
import python.tools.mulo as mulo
import python.webserver.formhandler
import copy

class MyServer(BaseHTTPRequestHandler):
    m_FormularHandler = {}
    m_CallbackHandler = {}
    def __init__(self, *args):
        """Constructor, resets the formular handler dictionary

                :return: -
                :rtype: -

                """
        self.m_CallbackHandler = MyServer.m_FormularHandler.copy()
        BaseHTTPRequestHandler.__init__(self, *args)

    def __del__(self):
        """Destructor

        :return: -
        :rtype: -

        """
        m_CallbackHandler = {}

    def do_GET(self):
        """Displays the content of the (templated) web site

        :return: -
        :rtype: -

        """
        if self.path.endswith('.css'):
            cssfilepath = '.' + self.path
            try:
                print(cssfilepath)
                f = open(cssfilepath)
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                csscontent = f.read()
                f.close()
                self.wfile.write(bytes(csscontent, 'utf-8'))
            except:
                file_to_open = "File Not Found"
                self.send_response(404)
                self.end_headers()

        else:
            if self.path == '/':
                self.path = './html/index.html'
            else:
                self.path = './html' + self.path

            try:
                #print(self.path[0:])
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

        :return: -
        :rtype: -

        """
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        self.keyvalue = dict(urllib.parse.parse_qsl(self.data_string))
        self.path = './html/profile.html'
        try:
            if b'FormIdentifier' in self.keyvalue:
                print('Key FormIdentifier exists with value {}'.format(self.keyvalue[b'FormIdentifier']))
                if self.keyvalue[b'FormIdentifier'] in self.m_CallbackHandler:
                    print('Executing callback')
                    callbacksel = self.keyvalue[b'FormIdentifier']
                    self.m_CallbackHandler[callbacksel].GetParameterSet(self.keyvalue)
                    status, file_to_open = self.m_CallbackHandler[callbacksel].CreateResponse()
                    if status == False:
                        file_to_open = "Unregistered web page"
                        self.send_response(404)
                    else:
                        print('Request OK')
                        self.send_response(200)

                else:
                    print('Page has no identifier')
            else:
                # unknown page
                print(self.path[1:])
                file_to_open = open(self.path[2:]).read()
                # song = self.keyvalue[b'songname'].decode('utf-8')
                # file_to_open = file_to_open.replace('{favouritesong}', song)
                self.send_response(200)
        except:
            file_to_open = "File Not Found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    @staticmethod
    def RegisterFormular(formularidentifier, formularhandler):
        if not formularidentifier in MyServer.m_FormularHandler:
            MyServer.m_FormularHandler[formularidentifier] = formularhandler
            print('Parameter {} registered'.format(formularidentifier))
        else:
            print('Error: Parameter {} already registered'.format(formularidentifier))

def StartupServer():
    """Starts the web server

        :return: -
        :rtype: -
        """
    server = python.webserver.HTTPWebServer()
    server.Initialize("localhost", 8080)
    MyServer.RegisterFormular(b'homepage_form', python.webserver.formhandler.HomepageHandler())
    MyServer.RegisterFormular(b'login_form', python.webserver.formhandler.LoginHandler())
    server.Start(MyServer)

def StartupRema():
    """Initializes spotify connection

        :return: -
        :rtype: -
        """
    spy = rema()
    [a,b,c,d] = spy.GetAttributes()
    for i,j,k,l in zip(a,b,c,d):
        print(i, j, k, l)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    """Entry point of the application

        :return: -
        :rtype: -
        """
    # mulo.CreatePlayList('D:\Data\Music', 'Playlist.json', True)
    # StartupRema()
    StartupServer()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
