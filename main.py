from python.webserver.sessionmanager import SessionManager
from python.webserver.eardriphttpserver import EarDripServer
import logging
import python.webserver
import python.webserver.formhandler


def StartupServer():
    """Starts the web server

        :return: -
        :rtype: -
        """
    logging.info('Starting up server')
    EarDripServer.RegisterForm(b'homepage_form', python.webserver.formhandler.HomepageHandler())
    EarDripServer.RegisterForm(b'trackselection_form', python.webserver.formhandler.TrackSelectionHandler())
    EarDripServer.RegisterForm(b'login_form', python.webserver.formhandler.LoginHandler())
    EarDripServer.RegisterForm(b'signup_form', python.webserver.formhandler.SignupHandler())
    EarDripServer.RegisterForm(b'profile_form', python.webserver.formhandler.ProfileHandler())
    EarDripServer.RegisterForm(b'algorithm_button_form', python.webserver.formhandler.AlgorithmHandler())
    EarDripServer.RegisterForm(b'how_to_use_form', python.webserver.formhandler.HowToUseForm())
    SessionManager.StartScheduer()
    server = python.webserver.HTTPWebServer()
    server.Initialize("localhost", 8080)
    server.Start(EarDripServer)
    SessionManager.StopScheduer()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    """Entry point of the application

        :return: -
        :rtype: -
        """
    # mulo.CreatePlayList('D:\Data\Music', 'Playlist.json', True)
    StartupServer()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
