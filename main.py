from http.server import BaseHTTPRequestHandler
from python.rema import remotedatabase as rema
from python.eddi import Eddi
from http.cookies import SimpleCookie
import logging
import urllib.parse
import python.webserver
import python.webserver.formhandler
from python.webserver.sessionmanager import SessionManager

class MyServer(BaseHTTPRequestHandler):
    m_SessionHandler = {}
    m_FormHandler = {}
    m_CallbackHandler = {}
    m_UserProfileInterface = None
    m_TrackProfileInterface = None
    m_ProfileInfo = None

    def __init__(self, *arguments):
        """Constructor, resets the formula handler dictionary

        :return: -
        :rtype: -

        """
        spy = StartupRema()
        self.m_CallbackHandler = MyServer.m_FormHandler.copy()
        dbaccess = Eddi()

        user_interface = dbaccess.GetUserAccessInterface()
        track_profile_interface = dbaccess.GetTrackAttributesAccessInterface()
        self.m_ProfileInfo = {'validity': False, 'username': 'empty', 'password': 'empty', 'email': 'empty'}

        for i in self.m_CallbackHandler:
            self.m_CallbackHandler[i].RegisterSpy(spy)
            self.m_CallbackHandler[i].RegisterUserAccessInterface(user_interface)
            self.m_CallbackHandler[i].RegisterTrackAttributesAccessInterface(track_profile_interface)
            self.m_CallbackHandler[i].RegisterProfile(self.m_ProfileInfo)

        BaseHTTPRequestHandler.__init__(self, *arguments)

    def __del__(self):
        """Destructor

        :return: -
        :rtype: -

        """
        m_CallbackHandler = {}

    def HandleSessionIdentifier(self):
        cookies = SimpleCookie(self.headers.get('Cookie'))
        if cookies and 'session_id' in cookies:
            session_id = SessionManager.OpenSession(cookies['session_id'].value, self.m_ProfileInfo)
            print("Session Id: {} User: {}".format(session_id, self.m_ProfileInfo['username']))
        else:
            session_id = SessionManager.OpenSession(None, self.m_ProfileInfo)
            print("Session Id: {} User: {}".format(session_id, self.m_ProfileInfo['username']))
            cookies['session_id'] = session_id
            for morsel in cookies.values():
                self.send_header("Set-Cookie", morsel.OutputString())

    def GetSessionIdentifier(self) -> int:
        session_identifier = None
        cookies = SimpleCookie(self.headers.get('Cookie'))
        if cookies and 'session_id' in cookies:
            session_identifier = cookies['session_id'].value
        return session_identifier

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
            set_access_denied_message = False
            identifier = self.GetSessionIdentifier()
            if identifier is not None:
                info = SessionManager.GetSessionContext(identifier)
                if info is not None:
                    self.m_ProfileInfo = info

            if self.path == '/':
                self.path = './html/index.html'
            elif self.path == '/index.html':
                self.path = './html/index.html'
            elif not self.m_ProfileInfo['validity']:
                self.path = './html/index.html'
                set_access_denied_message = True
            else:
                self.path = './html' + self.path

            try:
                file_to_open = open(self.path[0:]).read()
                if set_access_denied_message:
                    file_to_open = file_to_open.replace('<!-- LOGIN_STATUS -->', '<b>Acces denied. You are not signed '
                                                                                 'in.</b>')
                    logging.info('loading html file {}. Access denied.'.format(self.path[0:]))
                else:
                    logging.info('loading html file {}'.format(self.path[0:]))

                self.send_response(200)
                self.HandleSessionIdentifier()

            except:
                file_to_open = "File Not Found"
                logging.error('loading html file {} failed'.format(self.path[0:]))
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))
        return  # BaseHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        """Handles post requests of a web client. Extracts key value pairs of the request (has to be extended)

        :return: -
        :rtype: -

        """
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        self.keyvalue = dict(urllib.parse.parse_qsl(self.data_string))
        session_id = self.GetSessionIdentifier()
        try:
            if b'FormIdentifier' in self.keyvalue:
                logging.info('Key FormIdentifier exists with value {}'.format(self.keyvalue[b'FormIdentifier']))
                if self.keyvalue[b'FormIdentifier'] in self.m_CallbackHandler:
                    logging.info('Executing callback')
                    callbacksel = self.keyvalue[b'FormIdentifier']
                    self.m_CallbackHandler[callbacksel].GetParameterSet(session_id, self.keyvalue)
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
    MyServer.RegisterForm(b'trackselection_form', python.webserver.formhandler.TrackSelectionHandler())
    MyServer.RegisterForm(b'login_form', python.webserver.formhandler.LoginHandler())
    MyServer.RegisterForm(b'signup_form', python.webserver.formhandler.SignupHandler())
    MyServer.RegisterForm(b'profile_form', python.webserver.formhandler.ProfileHandler())
    SessionManager.StartScheduer()
    server.Start(MyServer)
    SessionManager.StopScheduer()


def StartupRema():
    """Initializes spotify connection

        :return: -
        :rtype: -
        """
    logging.info('Starting up rema')
    spy = rema()
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
