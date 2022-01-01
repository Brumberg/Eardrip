from abc import ABCMeta, abstractmethod

class GenericFormHandler:
    """This is a conceptual class representation of a generic form interface.
    Main purpose of the class is parameter extraction related to the opened web page and
    responding to the request by updating/reloading the html page

    """

    @abstractmethod
    def __init__(self):
        pass

    def __del__(self):
        pass

    @abstractmethod
    def GetParameterSet(self, paramset):
        """default initialization (e.g. reading config struct)

        """
        # print('Generic GetParamSet callback executed')
        pass

    @abstractmethod
    def CreateResponse(self):
        """default initialization (e.g. reading config struct)

        """
        # print('Generic CreateResponse executed')
        pass

class HomepageHandler(GenericFormHandler):
    def __init__(self):
        # print('Constructor of homepage handler called')
        pass

    def __del__(self):
        # print('Destructor of homepage handler called')
        pass

    def GetParameterSet(self, paramset):
        print('Homepage handler executed')
        for i in paramset:
            print(i)

    def CreateResponse(self):
        print('CreateResponse of homepage handler called')
        filecontent = []
        retVal = False
        try:
            filecontent = open('./html/profile.html').read()
            retVal = True
        except OSError:
            print("Unable to open file")
        return retVal, filecontent

class LoginHandler(GenericFormHandler):
    def __init__(self):
        # print('Constructor of login handler called')
        pass

    def __del__(self):
        # print('Destructor of login handler called')
        pass

    def GetParameterSet(self, paramset):
        print('GetParameterSet of login handler called')
        for i in paramset:
            print(i)

    def CreateResponse(self):
        print('CreateResponse of login handler called')
        filecontent = []
        retVal = False
        try:
            filecontent = open('./html/profile.html').read()
            retVal = True
        except OSError:
            print("Unable to open file")
        return retVal, filecontent

