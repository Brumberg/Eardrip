
from abc import ABC, abstractmethod
from http.server import BaseHTTPRequestHandler, HTTPServer

class GenericWebServer:
    """This is a conceptual class representation of a generic web server interface
    (HTTP). It just provides an abstraction for a real implementation

    """


    @abstractmethod
    def Initialize(self):
        """default initialization (e.g. reading config struct)

        """
        pass

    @abstractmethod
    def Initialize(self, hostname, serverPort):
        """extended initialization for the web interface

        :param hostName: overrides the default hostname
        :type: string
        :param serverPort: defines the communication port
        :type: int

        """
        pass

    @abstractmethod
    def Start(self, contentHandler):
        """Starts the web (http) server

        :param contentHandler: handling of web content
        :type: class
        :return: -
        :rtype: -

        """
        pass

class HTTPWebServer(GenericWebServer):
    """Actual implementation of the server interface (HTTP).
    It provides the real implementation

    """
    hostName = []
    serverPort = []
    def Initialize(self):
        """default initialization (e.g. reading config struct)

        """
        print("Start of web server.")

    def Initialize(self, hostname, serverPort):
        """extended initialization for the web interface

        :param hostName: overrides the default hostname
        :type: string
        :param serverPort: defines the communication port
        :type: int

        """
        self.hostName = hostname
        self.serverPort = serverPort

    def Start(self, contentHandler):

        """Starts the web (http) server

        :param contentHandler: handling of web content
        :type: class
        :return: -
        :rtype: -

        """
        webServer = HTTPServer((self.hostName, self.serverPort), contentHandler)
        print("Server started http://%s:%s" % (self.hostName, self.serverPort))

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Server stopped.")