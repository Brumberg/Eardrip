

from http.server import BaseHTTPRequestHandler
from python.rema import remotedatabase as rema
import logging
import urllib.parse
import python.webserver
import python.webserver.formhandler
import python.tools.mulo as mulo

class MyServer(BaseHTTPRequestHandler):
    m_FormHandler = {}
    m_CallbackHandler = {}
    def __init__(self, *arguments):
        """Constructor, resets the formular handler dictionary

        :return: -
        :rtype: -

        """
        spy = StartupRema()
        self.m_CallbackHandler = MyServer.m_FormHandler.copy()
        for i in self.m_CallbackHandler:
            self.m_CallbackHandler[i].RegisterSpy(spy)
        BaseHTTPRequestHandler.__init__(self, *arguments)

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
                logging.info('loading css file {}'.format(cssfilepath))
                f = open(cssfilepath)
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                csscontent = f.read()
                f.close()
                self.wfile.write(bytes(csscontent, 'utf-8'))
            except:
                file_to_open = "File Not Found"
                logging.error('CSS file {} not found'.format(cssfilepath))
                self.send_response(404)
                self.end_headers()

        else:
            if self.path == '/':
                self.path = './html/index.html'
            else:
                self.path = './html' + self.path

            try:
                file_to_open = open(self.path[0:]).read()
                logging.info('loading html file {}'.format(self.path[0:]))
                self.send_response(200)
            except:
                file_to_open = "File Not Found"
                logging.error('loading html file {} failed'.format(self.path[0:]))
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
        try:
            if b'FormIdentifier' in self.keyvalue:
                logging.info('Key FormIdentifier exists with value {}'.format(self.keyvalue[b'FormIdentifier']))
                if self.keyvalue[b'FormIdentifier'] in self.m_CallbackHandler:
                    logging.info('Executing callback')
                    callbacksel = self.keyvalue[b'FormIdentifier']
                    self.m_CallbackHandler[callbacksel].GetParameterSet(self.keyvalue)
                    status, file_to_open = self.m_CallbackHandler[callbacksel].CreateResponse()
                    if status == False:
                        file_to_open = "Unregistered web page"
                        self.send_response(404)
                    else:
                        logging.info('Request OK')
                        self.send_response(200)

                else:
                    logging.error('Page has no identifier')
            else:
                logging.warning('Requested page {} has no form identifier'.format(self.path))
                errorpage = 'html/profile.html'
                try:
                    file_to_open = open(errorpage).read()
                    logging.info('Responding with default error page')
                except:
                    file_to_open = 'Can not load default error page'
                    logging.error('Default error page does not exist')
                # song = self.keyvalue[b'songname'].decode('utf-8')
                # file_to_open = file_to_open.replace('{favouritesong}', song)
                self.send_response(200)
        except:
            file_to_open = "File Not Found"
            logging.error('Requested page {} has no form identifier'.format(self.path))
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    @staticmethod
    def RegisterForm(formidentifier, formhandler):
        """register handler for html page

        :param formidentifier: identifier of form section
        :type: string
        :param formhandler: manages post requests of web-forms
        :type: derived from GenericFormHandler

        """
        if not formidentifier in MyServer.m_FormHandler:
            MyServer.m_FormHandler[formidentifier] = formhandler
            logging.info('Parameter {} registered'.format(formidentifier))
        else:
            logging.error('Error: Parameter {} already registered'.format(formidentifier))

def StartupServer():
    """Starts the web server

        :return: -
        :rtype: -
        """
    logging.info('Starting up server')
    server = python.webserver.HTTPWebServer()
    server.Initialize("localhost", 8080)
    MyServer.RegisterForm(b'homepage_form', python.webserver.formhandler.HomepageHandler())
    MyServer.RegisterForm(b'login_form', python.webserver.formhandler.LoginHandler())
    MyServer.RegisterForm(b'profile_form', python.webserver.formhandler.ProfileHandler())
    server.Start(MyServer)

def StartupRema():
    """Initializes spotify connection

        :return: -
        :rtype: -
        """
    logging.info('Starting up rema')
    spy = rema()
    # just for testing
    # [a,b,c,d] = spy.GetAttributes('Nothing else matters')
    # for i,j,k,l in zip(a,b,c,d):
    #    print(i, j, k, l)
    return spy

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    """Entry point of the application

        :return: -
        :rtype: -
        """
    # mulo.CreatePlayList('D:\Data\Music', 'Playlist.json', True)
    StartupServer()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
