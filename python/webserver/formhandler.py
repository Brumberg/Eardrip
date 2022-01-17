from abc import ABCMeta, abstractmethod
from typing import Tuple
import python.rema

class GenericFormHandler:
    """This is a conceptual class representation of a generic form interface.
    Main purpose of the class is parameter extraction related to the opened web page and
    responding to the request by updating/reloading the html page

    """

    """storage for parameter request

    """
    m_ParameterSet = dict()
    m_ProfileInfo = dict()

    """spotify handler

    """
    m_Spy = []

    def __init__(self):
        """Constructor, resets the form handler dictionary

        :return: -
        :rtype: -

        """
        m_ParameterSet = {}

    def __del__(self):
        """Destructor, resets the form handler dictionary

        :return: -
        :rtype: -

        """
        self.m_ParameterSet = {}

    def RegisterProfile(self, profileinfo):
        """Register spy (spotify) object

        :param spy: object handles requests/inqueries to/from spotify
        :type: spy object
        :return: -
        :rtype: -

        """
        self.m_ProfileInfo = profileinfo


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
            track_name = self.m_ParameterSet[b'homepage_songtitle'].decode("utf-8")
            track_data = self.m_Spy.GetAttributes(track_name)
            track_uri = []
            artist_info = []
            artist_uri = []

            for i in range(0, len(track_data)):
                track_uri.append(track_data[i]['uri'])
                artist_uri.append(track_data[i]['artist_uri'])

            artist_info = self.m_Spy.GetArtistInfo(artist_uri)
            track_analysis = self.m_Spy.GetTrackAnalytics(track_uri)

            music_list = str()
            for i in range(0, len(track_data)):
                table_row = self.m_HTMLTableRowDescriptor
                table_row = table_row.replace('ARTIST_ID', track_data[i]['artist'])
                table_row = table_row.replace('TITLE_ID', track_data[i]['track'])
                table_row = table_row.replace('TRACK_ID', track_data[i]['track_id'])
                table_row = table_row.replace('GENRE_ID', ','.join(artist_info[i]['genres']))
                table_row = table_row.replace('POPULARITY', str(track_data[i]['popularity']))
                #table_row = table_row.replace('URI', track_data[i]['uri'])
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
            file_content = open('./html/profile.html').read()
            retVal = True
        except OSError:
            print("Unable to open file")
        return retVal, file_content

class ProfileHandler(GenericFormHandler):
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
        if self.m_ProfileInfo['Validated'] == True:
            file_content = []
            retVal = False
            try:
                file_content = open('./html/profile.html').read()
                retVal = True
            except OSError:
                print("Unable to open file")
            return retVal, file_content
        else:
            print('Error: Profile non existing')
            file_content = open('./html/profile.html').read()
            self.m_ProfileInfo['username'] = 'unknown'
            self.m_ProfileInfo['email'] = 'unknown'
            self.m_ProfileInfo['role'] = '-'
            self.m_ProfileInfo['Validated'] = False
            retVal = True

