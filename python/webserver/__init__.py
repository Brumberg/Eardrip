from abc import ABC, abstractmethod
from socketserver import ThreadingMixIn
from http.server import HTTPServer
import time
import threading
import logging


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
    class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
        """Handle requests in a separate thread."""

    """Actual implementation of the server interface (HTTP).
    It provides the real implementation

    """
    hostName = []
    serverPort = []
    webServer = None
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

    def StartSingleThreadedServer(self, contentHandler):
        self.webServer = HTTPServer((self.hostName, self.serverPort), contentHandler)
        print("Server started http://%s:%s" % (self.hostName, self.serverPort))
        try:
            self.webServer.serve_forever()
        except KeyboardInterrupt:
            pass

    def HTTPBackgroundWorker(self, contentHandler):
        self.webServer = HTTPWebServer.ThreadedHTTPServer((self.hostName, self.serverPort), contentHandler)
        print("Server started http://%s:%s" % (self.hostName, self.serverPort))
        try:
            self.webServer.serve_forever()
        except:
            #suppress error messages during termination
            pass
        logging.info('Shut down html background process')


    def StartMultiThreadedServer(self, contentHandler):
        stop_execution = False

        #def handler(signum, frame):
        #    nonlocal stop_execution
        #    print('Execution terminated')
        #    stop_execution=True

        #signal.signal(signal.SIGINT, handler)

        try:
            #signal.signal(signal.SIGINT, handler)
            httpthread = threading.Thread(target=self.HTTPBackgroundWorker,
                                      name='eardrip-http-backworker', daemon=True, args=(contentHandler,))
            httpthread.daemon = True
            httpthread.start()

            while not stop_execution:
                time.sleep(1)

        except (KeyboardInterrupt, SystemExit):
            pass

    def Start(self, contentHandler):

        """Starts the web (http) server

        :param contentHandler: handling of web content
        :type: class
        :return: -
        :rtype: -

        """
        #webServer = self.StartSingleThreadedServer(contentHandler)
        self.StartMultiThreadedServer(contentHandler)
        if self.webServer is not None:
            self.webServer.server_close()
        print("Server stopped.")
