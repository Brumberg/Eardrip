from abc import ABCMeta, abstractmethod
from typing import Tuple
import python.rema
import logging
import logging.handlers
import re


class GenericFormHandler:
    """This is a conceptual class representation of a generic form interface.
    Main purpose of the class is parameter extraction related to the opened web page and
    responding to the request by updating/reloading the html page

    """

    """storage for parameter request

    """
    m_ParameterSet = None
    m_ProfileInfo = None
    m_UserAccessInterface = None
    m_TrackAttributesAccessInterface = None

    """spotify handler

    """
    m_Spy = None

    def __init__(self):
        """Constructor, resets the form handler dictionary

        :return: -
        :rtype: -

        """
        self.m_ParameterSet = None

    def __del__(self):
        """Destructor, resets the form handler dictionary

        :return: -
        :rtype: -

        """
        self.m_ParameterSet = None

    def RegisterProfile(self, profile_info):
        """Register profile object

        :param profile_info: object registers user profile info
        :type: profile object
        :return: -
        :rtype: -

        """
        self.m_ProfileInfo = profile_info

    def RegisterSpy(self, spy):
        """Register spy (spotify) object

        :param spy: object handles requests/inqueries to/from spotify
        :type: spy object
        :return: -
        :rtype: -

        """
        self.m_Spy = spy

    def RegisterUserAccessInterface(self, interface):
        """Register userinterface  object

        :param spy: object handles requests/inqueries to/from spotify
        :type: spy object
        :return: -
        :rtype: -

        """
        self.m_UserAccessInterface = interface

    def RegisterTrackAttributesAccessInterface(self, interface):
        """Register spy (spotify) object

        :param interface:
        :type: interface object
        :return: -
        :rtype: -

        """
        self.m_TrackAttributesAccessInterface = interface

    @abstractmethod
    def GetParameterSet(self, param_set: dict):
        """extract parameter set and store it

        :param param_set: dictionary containing all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        self.m_ParameterSet = param_set.copy()

    @abstractmethod
    def CreateResponse(self) -> Tuple[bool, str]:
        """create html response

        :return: status, html content
        :rtype: boolean, string

        """
        pass


class HomepageHandler(GenericFormHandler):
    m_HTMLHeaderLine = (
        '<tr>'
        '<td>artist</td>'
        '<td>title</td>'
        '<td>track id</td>'
        '<td>genre</td>'
        '<td>popularity</td>'
        '<td>action</td>'
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
        '<td><form name="TABLE_FORM_ACTION" action="" method="post">'
        '<button>Track_ACTION</button>'
        '<input type="hidden" id="FormIdentifier" name="FormIdentifier" value="trackselection_form">'
        '<input type="hidden" value="TRACK_ID" name="field_track_id_NUMBER" id="field_track_id_NUMBER">'
        '<input type="hidden" value="ARTIST_ID_NUMBER" name="field_artist_id_NUMBER" id="field_artist_id_NUMBER">'
        '<input type="hidden"value="TITLE_ID" name="field_title_id_NUMBER" id="field_title_id_NUMBER">'
        '<input type="hidden"value="GENRE_ID" name="field_genre_id_NUMBER" id="field_genre_id_NUMBER">'
        '<input type="hidden"value="POPULARITY" name="field_popularity_NUMBER" id="field_popularity_NUMBER">'
        '<input type="hidden"value="DANCEABILITY" name="field_danceability_NUMBER" id="field_danceability_NUMBER">'
        '<input type="hidden"value="ENERGY" name="field_energy_NUMBER" id="field_energy_NUMBER">'
        '<input type="hidden"value="LIVENESS" name="field_liveness_NUMBER" id="field_liveness_NUMBER">'
        '<input type="hidden"value="MODE" name="field_mode_NUMBER" id="field_mode_NUMBER">'
        '<input type="hidden"value="TIME_SIGNATURE" name="field_time_signature_NUMBER" id="field_time_signature_NUMBER">'
        '<input type="hidden"value="TEMPO" name="field_tempo_NUMBER" id="field_tempo_NUMBER">'
        '<input type="hidden"value="VALENCE" name="field_valence_NUMBER" id="field_valence_NUMBER">'
        'ACTION</form></td>'
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
        super().__init__()

    def __del__(self):
        """Destructor, resets the form handler dictionary

        :return: -
        :rtype: -

        """
        super().__del__()

    def GetParameterSet(self, param_set: dict):
        """extract parameter set and store it

        :param paramset: dictionary containing all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        super().GetParameterSet(param_set)

    def CreateResponse(self) -> Tuple[bool, str]:
        """create html response

        :return: status, html content
        :rtype: boolean, string

        """
        file_content = []
        retVal = False
        try:
            file_content = open('./html/homepage.html').read()
            retVal = True
        except OSError:
            logging.debug('Homepage handler executed')

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
            track_analysis = self.m_Spy.GetTrackAnalytics(track_uri[0])

            music_list = str()
            for i in range(0, len(track_data)):
                table_row = self.m_HTMLTableRowDescriptor
                table_row = table_row.replace('ARTIST_ID', track_data[i]['artist'])
                table_row = table_row.replace('TITLE_ID', track_data[i]['track'])
                table_row = table_row.replace('TRACK_ID', track_data[i]['track_id'])
                table_row = table_row.replace('GENRE_ID', ','.join(artist_info[i]['genres']))
                table_row = table_row.replace('POPULARITY', str(track_data[i]['popularity']))
                table_row = table_row.replace('NUMBER', str(i))
                # table_row = table_row.replace('URI', track_data[i]['uri'])
                table_row = table_row.replace('ACTION', str(i))
                music_list = music_list + table_row

            table_header = self.m_HTMLHeaderLine
            table_header = table_header.replace('<!-- header_attachment_anchor -->', music_list)

            table = self.m_HTMLTableResponse
            table = table.replace('<!-- table_content_anchor -->', table_header)
            file_content = file_content.replace('<!-- homepage_result_table -->', table)
        return retVal, file_content


class TrackSelectionHandler(GenericFormHandler):
    m_HTMLHeaderLine = (
        '<tr>'
        '<td>artist</td>'
        '<td>title</td>'
        '<td>track id</td>'
        '<td>genre</td>'
        '<td>popularity</td>'
        '<td>action</td>'
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
        '<td><form name="TABLE_FORM_ACTION" action="" method="post">'
        '<button>Track_ACTION</button>'
        '<input type="hidden" id="FormIdentifier" name="FormIdentifier" value="homepage_form">'
        '<input type="hidden" value="TRACK_ID" name="field_track_id_NUMBER" id="field_track_id_NUMBER">'
        '<input type="hidden" value="ARTIST_ID_NUMBER" name="field_artist_id_NUMBER" id="field_artist_id_NUMBER">'
        '<input type="hidden"value="TITLE_ID" name="field_title_id_NUMBER" id="field_title_id_NUMBER">'
        '<input type="hidden"value="GENRE_ID" name="field_genre_id_NUMBER" id="field_genre_id_NUMBER">'
        '<input type="hidden"value="POPULARITY" name="field_popularity_NUMBER" id="field_popularity_NUMBER">'
        '<input type="hidden"value="DANCEABILITY" name="field_danceability_NUMBER" id="field_danceability_NUMBER">'
        '<input type="hidden"value="ENERGY" name="field_energy_NUMBER" id="field_energy_NUMBER">'
        '<input type="hidden"value="LIVENESS" name="field_liveness_NUMBER" id="field_liveness_NUMBER">'
        '<input type="hidden"value="MODE" name="field_mode_NUMBER" id="field_mode_NUMBER">'
        '<input type="hidden"value="TIME_SIGNATURE" name="field_time_signature_NUMBER" id="field_time_signature_NUMBER">'
        '<input type="hidden"value="TEMPO" name="field_tempo_NUMBER" id="field_tempo_NUMBER">'
        '<input type="hidden"value="VALENCE" name="field_valence_NUMBER" id="field_valence_NUMBER">'
        'ACTION</form></td>'
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
        super().__init__()

    def __del__(self):
        """Destructor, resets the form handler dictionary

        :return: -
        :rtype: -

        """
        super().__del__()

    def GetParameterSet(self, param_set: dict):
        """extract parameter set and store it

        :param paramset: dictionary containing all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        super().GetParameterSet(param_set)

    def ConvertDictionary(self):
        """returns a dictionary containing the database elements

        :return: status, html content
        :rtype: boolean, string

        """

        dict = {}
        for key, value in self.m_ParameterSet.items():
            a = key.decode("utf-8")
            match = re.search(r"_\d$", a)
            if match:
                a = a[0:match.start()]

            #dict[a] = value.decode("utf-8")
            temp = value.decode("utf-8")
            dict[a] = temp
        return dict

    def CreateResponse(self) -> Tuple[bool, str]:
        """create html response

        :return: status, html content
        :rtype: boolean, string

        """
        file_content = []
        return_value = False

        if self.m_ParameterSet:
            dataset = self.ConvertDictionary()
            dataset.pop('FormIdentifier', None)
            if (self.m_TrackAttributesAccessInterface.write(dataset)):
                try:
                    file_content = open('./html/homepage.html').read()
                except OSError:
                    return_value = False
                    logging.error('Unable to open home page')
            else:
                return_value = False
                logging.error('Dictionary is empty')
        else:
            return_value = False
            logging.error('Dictionary is empty')

        return return_value, file_content


class LoginHandler(GenericFormHandler):
    def __init__(self):
        """Constructor, resets the formula handler dictionary

        :return: -
        :rtype: -

        """
        super().__init__()

    def __del__(self):
        """Destructor, resets the formular handler dictionary

        :return: -
        :rtype: -

        """
        super().__del__()

    def GetParameterSet(self, param_set: dict):
        """extract parameter set and store it

        :param param_set:
        :param paramset: dictionarycontaining all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        super().GetParameterSet(param_set)

    def CreateResponse(self) -> Tuple[bool, str]:
        """create html response

        :return: status, html content
        :rtype: boolean, string

        """
        file_content = []
        return_value = False
        try:
            login_username = self.m_ParameterSet[b'login_usernameid'].decode('utf-8')
            login_password = self.m_ParameterSet[b'login_passwordid'].decode('utf-8')
            profile_data = {'validity': False, 'username': login_username, 'password': login_password,'email': 'unknown'}

            page_to_open = './html/homepage.html'
            # searches database for the username
            success = self.m_UserAccessInterface.check(profile_data)
            if success:
                if profile_data['username'] is None:
                    logging.debug("unknown user")
                    return_value = False
                    page_to_open = './html/index.html'
                elif profile_data['password'] is None:
                    logging.debug("no password")
                    return_value = False
                    page_to_open = './html/index.html'
                elif profile_data['username'] == login_username and profile_data['password'] == login_password:
                    logging.debug("log in successfull")
                    return_value = True
                    profile_data['validity'] = True
                    page_to_open = './html/homepage.html'
                elif profile_data['username'] != login_username:
                    return_value = False
                    logging.debug("unknown user")
                    page_to_open = './html/index.html'
                else:
                    return_value = False
                    logging.debug("invalid password")
                    page_to_open = './html/index.html'
            else:
                page_to_open = './html/index.html'
                return_value = False

            file_content = open(page_to_open).read()

        except OSError:
            logging.error("Unable to open file")
        return return_value, file_content


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

    def CreateResponse(self) -> Tuple[bool, str]:
        """create html response

        :return: status, html content
        :rtype: boolean, string

        """
        file_content = []

        signup_username = self.m_ParameterSet[b'signup_usernameid'].decode('utf-8')
        signup_password = self.m_ParameterSet[b'signup_passwordid'].decode('utf-8')
        signup_email = self.m_ParameterSet[b'signup_emailid'].decode('utf-8')
        profile_dictionary = dict(zip(['validity', 'username', 'password', 'email'],
                                      [False, signup_username, signup_password, signup_email]))
        #print(signup_username)
        #print(signup_password)
        #print(signup_email)

        # adds the variables to the user table in the database
        profile_data = {'validity': False, 'username': signup_username, 'password': signup_password,
                        'email': signup_email}

        return_value = self.m_DataBase.m_UserAccessInterface.read(profile_data)
        if return_value:
            return_value = self.m_Parent.m_DataBase.m_UserAccessInterface.write(profile_data)
            if return_value:
                profile_dictionary['validity'] = True
                file_content = open('./html/profile.html').read()
            else:
                profile_dictionary['validity'] = False
                logging.error("Unable to access data base")
                self.send_response(404)

            self.m_ProfileInfo.update(profile_dictionary)
        else:
            logging.error('Unable to access database')

        self.m_ProfileInfo.update(profile_data)
        return return_value, file_content


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
        super().__init__()

    def __del__(self):
        """Destructor, resets the formula handler dictionary

        :return: -
        :rtype: -

        """
        super().__del__()

    def GetParameterSet(self, param_set: dict):
        """extract parameter set and store it

        :param paramset: dictionarycontaining all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        super().GetParameterSet(param_set)

    def CreateResponse(self) -> Tuple[bool, str]:
        """create html response

        :return: status, html content
        :rtype: boolean, string

        """
        file_content = []
        return_value = False
        if self.m_ProfileInfo['validate']:
            try:
                file_content = open('./html/profile.html').read()
                return_value = True
            except OSError:
                return_value = False
                logging.error("Unable to open profile page")

            if return_value:
                details_list = str()
                table_row = self.m_HTMLTableRowDescriptor
                table_row = table_row.replace('USERNAME', self.m_ProfileInfo['username'])
                table_row = table_row.replace('PASSWORD', self.m_ProfileInfo['password'])
                table_row = table_row.replace('EMAIL', self.m_ProfileInfo['email'])
                details_list = table_row

                table_header = self.m_HTMLHeaderLine
                table_header = table_header.replace('<!-- header_attachment_anchor -->', details_list)

                table = self.m_HTMLTableResponse
                table = table.replace('<!-- table_content_anchor -->', table_header)
                file_content = file_content.replace('<!-- profile_result_table -->', table)
            else:
                try:
                    file_content = open('./html/index.html').read()
                    return_value = True
                except OSError:
                    return_value = False
                    logging.error("Unable to open index page")

        return return_value, file_content


class LogoutHandler(GenericFormHandler):
    def __init__(self):
        """Constructor, resets the formular handler dictionary

        :return: -
        :rtype: -

        """
        super().__init__()

    def __del__(self):
        """Destructor, resets the formular handler dictionary

        :return: -
        :rtype: -

        """
        super().__del__()

    def GetParameterSet(self, param_set: dict):
        """extract parameter set and store it

        :param paramset: dictionarycontaining all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        super().GetParameterSet(param_set)

    def CreateResponse(self) -> Tuple[bool, str]:
        """create html response

        :return: status, html content
        :rtype: boolean, string

        """
        logging.debug('CreateResponse of logout handler called')
        file_content = []
        return False


class SongHandler(GenericFormHandler):
    def __init__(self):
        """Constructor, resets the formular handler dictionary

        :return: -
        :rtype: -

        """
        # print('Constructor of logout handler called')
        super().__init__()

    def __del__(self):
        """Destructor, resets the formular handler dictionary

        :return: -
        :rtype: -

        """
        # print('Destructor of logout handler called')
        super().__del__()

    def GetParameterSet(self, param_set: dict):
        """extract parameter set and store it

        :param paramset: dictionarycontaining all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        super().GetParameterSet(param_set)

    def CreateResponse(self) -> Tuple[bool, str]:
        """create html response

        :return: status, html content
        :rtype: boolean, string

        """
        logging.debug('CreateResponse of logout handler called')

        logging.debug('CreateResponse of logout handler called')
        return False
