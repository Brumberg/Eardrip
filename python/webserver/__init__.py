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

        :return: -
        :rtype: -

        """
        pass

    @abstractmethod
    def Initialize(self, hostname, serverPort):
        """extended initialization for the web interface

        :param hostName: overrides the default hostname
        :type: string
        :param serverPort: defines the communication port
        :type: int
        :return: -
        :rtype: -

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
    """HTTPWebServer redirects finally queries to the eardrip server. Thus, it is a wrapper class

    """

    class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
        """Handle requests in a separate thread - if a multithreaded server is chosen"""

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
        :param: serverPort: defines the communication port
        :type: int
        :return: -
        :rtype: -

        """
        self.hostName = hostname
        self.serverPort = serverPort

    def StartSingleThreadedServer(self, contentHandler):
        """instantiates the single threaded http server

        :param contentHandler: handle to the eardrip server
        :return: -
        :rtype: -

        """
        self.webServer = HTTPServer((self.hostName, self.serverPort), contentHandler)
        print("Server started http://%s:%s" % (self.hostName, self.serverPort))
        try:
            self.webServer.serve_forever()
        except KeyboardInterrupt:
            pass

    def HTTPBackgroundWorker(self, contentHandler):
        """background worker thread for http server to avoid blocking the main thread

        :param contentHandler: handle to the eardrip server
        :return: -
        :rtype: -

        """
        self.webServer = HTTPWebServer.ThreadedHTTPServer((self.hostName, self.serverPort), contentHandler)
        print("Server started http://%s:%s" % (self.hostName, self.serverPort))
        try:
            self.webServer.serve_forever()
        except:
            #suppress error messages during termination
            pass
        logging.info('Shut down html background process')


    def StartMultiThreadedServer(self, contentHandler):
        """instantiates the multithreaded http server by creating a thread that activates the server
        The HTTPBackgroundWorker finally instantiates the server

          :param contentHandler: handle to the eardrip server
          :return: -
          :rtype: -

          """
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

        :param contentHandler: handle to (eardrip) server class (handles html content)
        :type: class
        :return: -
        :rtype: -

        """
        #webServer = self.StartSingleThreadedServer(contentHandler)
        self.StartMultiThreadedServer(contentHandler)
        if self.webServer is not None:
            self.webServer.server_close()
        print("Server stopped.")
