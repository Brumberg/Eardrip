from abc import ABCMeta, abstractmethod
import python.rema
import mysql.connector
from typing import Tuple
class GenericFormHandler:
    """This is a conceptual class representation of a generic form interface.
    Main purpose of the class is parameter extraction related to the opened web page and
    responding to the request by updating/reloading the html page

    """

    """storage for parameter request

    """
    m_ParameterSet = dict()
    m_profileinfo = dict()

    # connects python to the database
    m_Db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Root",
        database="testdatabase"
    )
    m_Mycursor = m_Db.cursor()

    """spotify handler

    """
    m_Spy = []

    def __init__(self):
        """Constructor, resets the form handler dictionary

        :return: -
        :rtype: -

        """
        m_ParameterSet = {}

    # connects python to the database
        self.m_Db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Root",
            database="testdatabase"
        )
        self.m_Mycursor = self.m_Db.cursor()

    def __del__(self):
        """Destructor, resets the form handler dictionary

        :return: -
        :rtype: -

        """
        self.m_ParameterSet = {}

    def RegisterProfile(self, profileinfo):
        """Register profile object

        :param profile: object registers user profile info
        :type: profile object
        :return: -
        :rtype: -

        """
        self.m_profileinfo = profileinfo

    def RegisterSpy(self, spy):
        """Register spy (spotify) object

        :param spy: object handles requests/inqueries to/from spotify
        :type: spy object
        :return: -
        :rtype: -

        """
        self.m_Spy = spy

    @abstractmethod
    def GetParameterSet(self, param_set: dict):
        """extract parameter set and store it

        :param param_set: dictionary containing all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        # print('Generic GetParamSet callback executed')
        self.m_ParameterSet = param_set.copy()

    @abstractmethod
    def CreateResponse(self) -> Tuple[bool, str]:
        """create html response

        :return: status, html content
        :rtype: boolean, string

        """
        # print('Generic CreateResponse executed')
        pass

class HomepageHandler(GenericFormHandler):
    m_HTMLHeaderLine = (
        '<tr>'
        '<td>artist</td>'
        '<td>title</td>'
        '<td>track id</td>'
        '<td>genre</td>'
        '<td>popularity</td>'
        '</tr>'
        '<!-- header_attachment_anchor -->'
    )
    m_HTMLTableRowDescriptor = (
        '<tr>'
        '<td>ARTIST_ID</td>'
        '<td>TITLE_ID</td>'
        '<td>TRACK_ID</td>'
        '<td>GENRE_ID</td>'
        '<td>POPULARITY</td>'
        '</tr>'
    )
    m_HTMLTableResponse = (
        '<table style="width:100%">'
        '<!-- table_content_anchor -->'
        '</table>'
    )

    def __init__(self):
        """Constructor, resets the form handler dictionary

        :return: -
        :rtype: -

        """
        # print('Constructor of homepage handler called')
        super().__init__()

    def __del__(self):
        """Destructor, resets the form handler dictionary

        :return: -
        :rtype: -

        """
        # print('Destructor of homepage handler called')
        super().__del__()

    def GetParameterSet(self, param_set: dict):
        """extract parameter set and store it

        :param paramset: dictionary containing all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        super().GetParameterSet(param_set)
        print('Homepage handler executed')

    def CreateResponse(self) -> Tuple[bool, str]:
        """create html response

        :return: status, html content
        :rtype: boolean, string

        """
        print('CreateResponse of homepage handler called')
        file_content = []
        retVal = False
        try:
            file_content = open('./html/homepage.html').read()
            retVal = True
        except OSError:
            print("Unable to open file")

        if retVal:
            mycursor = self.m_Mycursor
            db = self.m_Db
            track_name = self.m_ParameterSet[b'homepage_songtitle'].decode("utf-8")
            [artist_name, track_name, popularity, track_id] = self.m_Spy.GetAttributes(track_name)

            music_list = str()
            for i in range(0, len(artist_name)):
                table_row = self.m_HTMLTableRowDescriptor
                table_row = table_row.replace('ARTIST_ID', artist_name[i])
                table_row = table_row.replace('TITLE_ID', track_name[i])
                table_row = table_row.replace('TRACK_ID', track_id[i])
                table_row = table_row.replace('GENRE_ID', 'pop')
                table_row = table_row.replace('POPULARITY', str(popularity[i]))
                music_list = music_list+table_row

            table_header = self.m_HTMLHeaderLine
            table_header = table_header.replace('<!-- header_attachment_anchor -->', music_list)

            table = self.m_HTMLTableResponse
            table = table.replace('<!-- table_content_anchor -->', table_header)
            file_content = file_content.replace('<!-- homepage_result_table -->', table)
        return retVal, file_content

class LoginHandler(GenericFormHandler):
    def __init__(self):
        """Constructor, resets the formular handler dictionary

        :return: -
        :rtype: -

        """
        # print('Constructor of login handler called')
        super().__init__()

    def __del__(self):
        """Destructor, resets the formular handler dictionary

        :return: -
        :rtype: -

        """
        # print('Destructor of login handler called')
        super().__del__()

    def GetParameterSet(self, param_set: dict):
        """extract parameter set and store it

        :param paramset: dictionarycontaining all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        super().GetParameterSet(param_set)
        print('GetParameterSet of login handler called')
        for i in param_set:
            print(i)

    def CreateResponse(self) -> Tuple[bool, str]:
        """create html response

        :return: status, html content
        :rtype: boolean, string

        """
        print('CreateResponse of login handler called')
        file_content = []
        retVal = False
        try:
            mycursor = self.m_Mycursor
            db = self.m_Db
            login_username = self.m_ParameterSet[b'login_usernameid'].decode('utf-8')
            login_password = self.m_ParameterSet[b'login_passwordid'].decode('utf-8')

            # searches database for the username
            mycursor.execute("SELECT * FROM user WHERE username = '%s'" % login_username)
            real_login_username = mycursor.fetchone()

            if real_login_username == None:
                print("INVALID USERNAME")

            elif real_login_username[1] == login_password:
                print("SUCCESSFUL")
                profile_username = login_username
                profile_password = login_password
            else:
                print("INVALID PASSWORD")

            mycursor.reset()
            file_content = open('./html/homepage.html').read()
            retVal = True
        except OSError:
            print("Unable to open file")
        return retVal, file_content

class SignupHandler(GenericFormHandler):
    def __init__(self):
        """Constructor, resets the formular handler dictionary

        :return: -
        :rtype: -

        """
        # print('Constructor of signup handler called')
        super().__init__()

    def __del__(self):
        """Destructor, resets the formular handler dictionary

        :return: -
        :rtype: -

        """
        # print('Destructor of signup handler called')
        super().__del__()

    def GetParameterSet(self, param_set: dict):
        """extract parameter set and store it

        :param paramset: dictionarycontaining all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        super().GetParameterSet(param_set)
        print('GetParameterSet of signup handler called')
        for i in param_set:
            print(i)

    def CreateResponse(self) -> Tuple[bool, str]:
        """create html response

        :return: status, html content
        :rtype: boolean, string

        """
        print('CreateResponse of signup handler called')
        file_content = []
        retVal = False
        try:
            mycursor = self.m_Mycursor
            db = self.m_Db
            signup_username = self.m_ParameterSet[b'signup_usernameid'].decode('utf-8')
            signup_password = self.m_ParameterSet[b'signup_passwordid'].decode('utf-8')
            signup_email = self.m_ParameterSet[b'signup_emailid'].decode('utf-8')

            print(signup_username)
            print(signup_password)
            print(signup_email)


            # adds the variables to the user table in the database
            mycursor.execute("INSERT INTO user (username, password, email) VALUES (%s, %s, %s)", (signup_username, signup_password, signup_email))
            db.commit()


            file_content = open('./html/profile.html').read()
            retVal = True
        except OSError:
            print("Unable to open file")
            self.send_response(404)
        return retVal, file_content


class ProfileHandler(GenericFormHandler):

    m_HTMLHeaderLine = (
        '<tr>'
        '<td>USERNAME</td>'
        '<td>PASSWORD</td>'
        '<td>EMAIL</td>'
        '</tr>'
        '<!-- header_attachment_anchor -->'
    )
    m_HTMLTableRowDescriptor = (
        '<tr>'
        '<td>USERNAME</td>'
        '<td>PASSWORD</td>'
        '<td>EMAIL</td>'
        '</tr>'
    )
    m_HTMLTableResponse = (
        '<table style="width:100%">'
        '<!-- table_content_anchor -->'
        '</table>'
    )

    def __init__(self):
        """Constructor, resets the formular handler dictionary

        :return: -
        :rtype: -

        """

        # print('Constructor of profile handler called')
        super().__init__()

    def __del__(self):
        """Destructor, resets the formular handler dictionary

        :return: -
        :rtype: -

        """
        # print('Destructor of profile handler called')
        super().__del__()

    def GetParameterSet(self, param_set: dict):
        """extract parameter set and store it

        :param paramset: dictionarycontaining all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        super().GetParameterSet(param_set)
        print('GetParameterSet of profile handler called')
        for i in param_set:
            print(i)

    def CreateResponse(self) -> Tuple[bool, str]:
        """create html response

        :return: status, html content
        :rtype: boolean, string

        """
        print('CreateResponse of profile handler called')
        file_content = []
        retVal = False
        try:
            file_content = open('./html/profile.html').read()
            retVal = True
        except OSError:
            print("Unable to open file")

        if retVal:
            mycursor = self.m_Mycursor
            db = self.m_Db
            username1 = ("sam cliffe")

            mycursor.execute("SELECT password FROM user WHERE username = '%s'" % username1)
            profile_password = mycursor.fetchone()
            profile_password = ''.join(profile_password)
            mycursor.reset()

            mycursor.execute("SELECT email FROM user WHERE username = '%s'" % username1)
            profile_email = mycursor.fetchone()
            profile_email = ''.join(profile_email)

            details_list = str()
            table_row = self.m_HTMLTableRowDescriptor
            table_row = table_row.replace('USERNAME', username1)
            table_row = table_row.replace('PASSWORD', profile_password)
            table_row = table_row.replace('EMAIL', profile_email)
            details_list = details_list+table_row

            table_header = self.m_HTMLHeaderLine
            table_header = table_header.replace('<!-- header_attachment_anchor -->', details_list)

            table = self.m_HTMLTableResponse
            table = table.replace('<!-- table_content_anchor -->', table_header)
            file_content = file_content.replace('<!-- profile_result_table -->', table)
        return retVal, file_content
