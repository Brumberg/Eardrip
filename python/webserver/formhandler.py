import uuid
from abc import ABCMeta, abstractmethod
from typing import Tuple
from python.webserver.sessionmanager import SessionManager
import time
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
    m_SessionId = None
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

        :param spy: object handles requests/inquiries to/from spotify
        :type: spy object
        :return: -
        :rtype: -

        """
        self.m_Spy = spy

    def RegisterUserAccessInterface(self, interface):
        """Register userinterface  object

        :param interface: object handles requests/inquiries to/from spotify
        :type: spy object
        :return: -
        :rtype: -

        """
        self.m_UserAccessInterface = interface

    def RegisterTrackAttributesAccessInterface(self, interface):
        """Register spy (spotify) object

        :param interface: interface to track handler (must contain read/write signature)
        :type: interface object
        :return: -
        :rtype: -

        """
        self.m_TrackAttributesAccessInterface = interface

    @abstractmethod
    def GetParameterSet(self, session_id: uuid, param_set: dict):
        """extract parameter set and store it

        :param session_id: unique identifier representing the session
        :type: uuid
        :param param_set: dictionary containing all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        self.m_ParameterSet = param_set.copy()
        self.m_SessionId = session_id
        self.m_ProfileInfo = SessionManager.GetSessionContext(session_id)
        #self.m_user_tracks_selected

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
        '<td>LINK</td>'
        '<td>GENRE_ID</td>'
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

    def GetParameterSet(self, session_id: uuid, param_set: dict):
        """extract parameter set and store it

        :param session_id: unique identifier for the session
        :type: uuid
        :param param_set: dictionary containing all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        super().GetParameterSet(session_id, param_set)

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

            artist = self.m_Spy.GetArtistInfo(artist_uri)
            track_analysis = self.m_Spy.GetTrackAnalytics(track_uri)

            track_selected_list = []
            artist_info = self.m_Spy.GetArtistInfo(artist_uri)
            track_analysis = self.m_Spy.GetTrackAnalytics(track_uri)
            retVal, track_selected_list = self.m_TrackAttributesAccessInterface.read(self.m_ProfileInfo["userID"])

            if len(track_selected_list) > 0:
                trackselectiontable = SelectedTrackHandler.FillInHTMLForm(track_selected_list)
                file_content = file_content.replace('<!-- homepage_selected_tracks_table -->', trackselectiontable)

            if len(track_data) > 0:
                htmltable = TrackSelectionHandler.FillInHTMLForm(track_data, artist_info, track_analysis, self.m_ProfileInfo["userID"])
                file_content = file_content.replace('<!-- homepage_result_table -->', htmltable)

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
        '<button>dislike</button>'
        '<button name="tlike" value="tlike">like</button>'
        '<input type="hidden" id="FormIdentifier" name="FormIdentifier" value="trackselection_form">'
        '<input type="hidden" id="userID_NUMBER" name="userID_NUMBER" value="USERID">'
        '<input type="hidden" value="TRACK_ID" name="field_track_id_NUMBER" id="field_track_id_NUMBER">'
        '<input type="hidden" value="ARTIST_ID" name="field_artist_id_NUMBER" id="field_artist_id_NUMBER">'
        '<input type="hidden"value="TITLE_ID" name="field_title_id_NUMBER" id="field_title_id_NUMBER">'
        '<input type="hidden"value="GENRE_ID" name="field_genre_id_NUMBER" id="field_genre_id_NUMBER">'
        '<input type="hidden"value="POPULARITY" name="field_popularity_NUMBER" id="field_popularity_NUMBER">'
        '<input type="hidden"value="DANCEABILITY" name="field_danceability_NUMBER" id="field_danceability_NUMBER">'
        '<input type="hidden"value="ENERGY" name="field_energy_NUMBER" id="field_energy_NUMBER">'
        '<input type="hidden"value="KEY" name="field_key_NUMBER" id="field_key_NUMBER">'
        '<input type="hidden"value="LOUDNESS" name="field_loudness_NUMBER" id="field_loudness_NUMBER">'
        '<input type="hidden"value="MODE" name="field_mode_NUMBER" id="field_mode_NUMBER">'
        '<input type="hidden"value="SPEECHINESS" name="field_speechiness_NUMBER" id="field_speechiness_NUMBER">'
        '<input type="hidden"value="ACOUSTICNESS" name="field_acousticness_NUMBER" id="field_acousticness_NUMBER">'
        '<input type="hidden"value="INSTRUMENTALNESS" name="field_instrumentalness_NUMBER" id="field_instrumentalness_NUMBER">'
        '<input type="hidden"value="LIVENESS" name="field_liveness_NUMBER" id="field_liveness_NUMBER">'
        '<input type="hidden"value="VALENCE" name="field_valence_NUMBER" id="field_valence_NUMBER">'
        '<input type="hidden"value="TEMPO" name="field_tempo_NUMBER" id="field_tempo_NUMBER">'
        '<input type="hidden"value="TYPE" name="field_type_NUMBER" id="field_type_NUMBER">'
        '<input type="hidden"value="ATTRIB_ID" name="field_id_NUMBER" id="field_id_NUMBER">'
        '<input type="hidden"value="ATTRIB_URI" name="field_uri_NUMBER" id="field_uri_NUMBER">'
        '<input type="hidden"value="TRACK_HREF" name="field_track_href_NUMBER" id="field_trackhref_NUMBER">'
        '<input type="hidden"value="ANALYSIS_URL" name="field_analysis_url_NUMBER" id="field_analysisurl_NUMBER">'
        '<input type="hidden"value="DURATION_MS" name="field_duration_ms_NUMBER" id="field_durationms_NUMBER">'
        '<input type="hidden"value="TIME_SIGNATURE" name="field_time_signature_NUMBER" id="field_time_signature_NUMBER">'  
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

    def GetParameterSet(self, session_id: int, param_set: dict):
        """extract parameter set and store it

        :param session_id: unique identifier representing the session
        :type: uuid
        :param param_set: set of parameters received from the user
        :type: dict
        :return: -
        :rtype: -

        """
        super().GetParameterSet(session_id, param_set)

    @classmethod
    def FillInHTMLForm(cls, track_data: list, artist_info: list, track_analysis: list, userID: str) -> str:
        """

        :param track_data: contain list of tracks
        :type: list
        :param artist_info: related artist attributes
        :type: list
        :param track_analysis: extended track attributes
        :type: list
        :return: string containing filled in html table
        :rtype: string
        """
        music_list = str()
        for i in range(0, len(track_data)):
            table_row = TrackSelectionHandler.m_HTMLTableRowDescriptor
            table_row = table_row.replace('ARTIST_ID', track_data[i]['artist'])
            table_row = table_row.replace('TITLE_ID', track_data[i]['track'])
            table_row = table_row.replace('TRACK_ID', track_data[i]['track_id'])
            table_row = table_row.replace('GENRE_ID', ','.join(artist_info[i]['genres']))
            table_row = table_row.replace('POPULARITY', str(track_data[i]['popularity']))

            # table_row = table_row.replace('URI', track_data[i]['uri'])
            table_row = table_row.replace('DANCEABILITY', str(track_analysis[i]['danceability']))
            table_row = table_row.replace('ENERGY', str(track_analysis[i]['energy']))
            table_row = table_row.replace('KEY', str(track_analysis[i]['key']))
            table_row = table_row.replace('LOUDNESS', str(track_analysis[i]['loudness']))
            table_row = table_row.replace('MODE', str(track_analysis[i]['mode']))
            table_row = table_row.replace('SPEECHINESS', str(track_analysis[i]['speechiness']))
            table_row = table_row.replace('ACOUSTICNESS', str(track_analysis[i]['acousticness']))
            table_row = table_row.replace('INSTRUMENTALNESS', str(track_analysis[i]['instrumentalness']))
            table_row = table_row.replace('LIVENESS', str(track_analysis[i]['liveness']))
            table_row = table_row.replace('VALENCE', str(track_analysis[i]['valence']))
            table_row = table_row.replace('TEMPO', str(track_analysis[i]['tempo']))
            table_row = table_row.replace('TYPE', str(track_analysis[i]['type']))
            table_row = table_row.replace('ATTRIB_ID', str(track_analysis[i]['id']))
            table_row = table_row.replace('ATTRIB_URI', str(track_analysis[i]['uri']))
            table_row = table_row.replace('TRACK_HREF', str(track_analysis[i]['track_href']))
            table_row = table_row.replace('ANALYSIS_URL', str(track_analysis[i]['analysis_url']))
            table_row = table_row.replace('DURATION_MS', str(track_analysis[i]['duration_ms']))
            table_row = table_row.replace('TIME_SIGNATURE', str(track_analysis[i]['time_signature']))
            table_row = table_row.replace('USERID', str(userID))

            table_row = table_row.replace('NUMBER', str(i))
            table_row = table_row.replace('ACTION', str(i))
            music_list = music_list + table_row

        table_header = TrackSelectionHandler.m_HTMLHeaderLine
        table_header = table_header.replace('<!-- header_attachment_anchor -->', music_list)

        table = TrackSelectionHandler.m_HTMLTableResponse
        table = table.replace('<!-- table_content_anchor -->', table_header)

        return table

    def ConvertDictionary(self):
        """returns a dictionary containing the database elements

        :return: status, html content
        :rtype: boolean, string

        """

        dict = {}
        for key, value in self.m_ParameterSet.items():
            a = key.decode("utf-8")
            match = re.search (r"_\d$", a)
            if match:
                a = a[0:match.start()]

            dict[a] = value.decode("utf-8")

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
            if self.m_TrackAttributesAccessInterface.write(dataset):
                try:
                    file_content = open('./html/homepage.html').read()
                    return_value = True
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

class SelectedTrackHandler(GenericFormHandler):
    m_HTMLSelectedTracksHeaderLine = (
        '<tr>'
        '<td>artist</td>'
        '<td>title</td>'
        '<td>track id</td>'
        '<td>genre</td>'
        '<td>popularity</td>'
        '</tr>'
        '<!-- header_attachment_anchor -->'
    )
    m_HTMLTrackSelectedTableRowDescriptor = (
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
        super().__init__()

    def __del__(self):
        """Destructor, resets the form handler dictionary

        :return: -
        :rtype: -

        """
        super().__del__()

    def GetParameterSet(self, session_id: int, param_set: dict):
        """extract parameter set and store it

        :param session_id: unique identifier representing the session
        :type: uuid
        :param param_set: set of parameters received from the user
        :type: dict
        :return: -
        :rtype: -

        """
        super().GetParameterSet(session_id, param_set)

    @classmethod
    def FillInHTMLForm(cls, selected_tracks_dictionary_list) -> str:
        """

        :param track_data: contain list of tracks
        :type: list
        :param artist_info: related artist attributes
        :type: list
        :param track_analysis: extended track attributes
        :type: list
        :return: string containing filled in html table
        :rtype: string
        """

        track_selected_list = str()
        for i in selected_tracks_dictionary_list:
            table_row = SelectedTrackHandler.m_HTMLTrackSelectedTableRowDescriptor
            table_row = table_row.replace('ARTIST_ID', i["field_artist_id"])
            table_row = table_row.replace('TITLE_ID', i["field_title_id"])
            table_row = table_row.replace('TRACK_ID', i["field_track_id"])
            table_row = table_row.replace('GENRE_ID', i["field_genre_id"])
            table_row = table_row.replace('POPULARITY', i["field_popularity"])

            track_selected_list = track_selected_list + table_row

        table_header = SelectedTrackHandler.m_HTMLSelectedTracksHeaderLine
        table_header = table_header.replace('<!-- header_attachment_anchor -->', track_selected_list)

        table = SelectedTrackHandler.m_HTMLTableResponse
        table = table.replace('<!-- table_content_anchor -->', table_header)

        return table

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

            dict[a] = value.decode("utf-8")
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
            if self.m_TrackAttributesAccessInterface.write(dataset):
                try:
                    file_content = open('./html/homepage.html').read()
                    return_value = True
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

class AlgorithmHandler(GenericFormHandler):
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
    m_SessionId = None
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

        :param spy: object handles requests/inquiries to/from spotify
        :type: spy object
        :return: -
        :rtype: -

        """
        self.m_Spy = spy

    def RegisterUserAccessInterface(self, interface):
        """Register userinterface  object

        :param interface: object handles requests/inquiries to/from spotify
        :type: spy object
        :return: -
        :rtype: -

        """
        self.m_UserAccessInterface = interface

    def RegisterTrackAttributesAccessInterface(self, interface):
        """Register spy (spotify) object

        :param interface: interface to track handler (must contain read/write signature)
        :type: interface object
        :return: -
        :rtype: -

        """
        self.m_TrackAttributesAccessInterface = interface

    @abstractmethod
    def GetParameterSet(self, session_id: uuid, param_set: dict):
        """extract parameter set and store it

        :param session_id: unique identifier representing the session
        :type: uuid
        :param param_set: dictionary containing all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        self.m_ParameterSet = param_set.copy()
        self.m_SessionId = session_id
        self.m_ProfileInfo = SessionManager.GetSessionContext(session_id)
        #self.m_user_tracks_selected

    def SpotifyFilter(self):

        retVal, track_selected_list = self.m_TrackAttributesAccessInterface.read(self.m_ProfileInfo["userID"])

        cycled_genres = {}
        most_popular_genre = ()
        most_popular_genre_count = ()
        genre_list = []
        genre_list_temp = []

        for i in track_selected_list:
            returned_genres = (i["field_genre_id"])
            genre_list_temp = returned_genres.split(",")
            genre_list = genre_list + genre_list_temp

        for z in genre_list:

            current_genre = z
            if current_genre not in cycled_genres:
                cycled_genres[current_genre] = 1


            else:
                cycled_genres[current_genre] = cycled_genres[current_genre] + (1)

        sorted_cycled_genres = sorted(cycled_genres.items(), key = lambda x:x[1], reverse = True)

        print(sorted_cycled_genres)

        top_genre = sorted_cycled_genres[0][0]
        print(top_genre)

        return retVal, file_content
    @abstractmethod
    def CreateResponse(self) -> Tuple[bool, str]:
        """create html response

        :return: status, html content
        :rtype: boolean, string

        """



        return self.SpotifyFilter()

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

    def GetParameterSet(self, session_id: uuid, param_set: dict):
        """extract parameter set and store it

        :param session_id: unique session identifier
        :type: uuid
        :param param_set: dictionary containing all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        super().GetParameterSet(session_id, param_set)

    def CreateResponse(self) -> Tuple[bool, str]:
        """create html response

        :return: status, html content
        :rtype: boolean, string

        """
        file_content = []
        return_value = False
        if b'login_usernameid' in self.m_ParameterSet and b'login_passwordid' in self.m_ParameterSet:
            try:
                login_username = self.m_ParameterSet[b'login_usernameid'].decode('utf-8')
                login_password = self.m_ParameterSet[b'login_passwordid'].decode('utf-8')
                profile_data = {'validity': False, 'username': login_username, 'password': login_password, 'email': 'unknown'}

                page_to_open = './html/index.html'
                # searches database for the username
                success = self.m_UserAccessInterface.read(profile_data)
                if success:
                    set_error_status = None
                    if profile_data['username'] is None:
                        logging.debug('Username not filled in.')
                        set_error_status = 'Username not filled in.'
                        return_value = True
                        page_to_open = './html/index.html'
                    elif profile_data['password'] is None:
                        logging.debug('Password not filled in')
                        set_error_status = 'Password not filled in.'
                        return_value = True
                        page_to_open = './html/index.html'
                    elif profile_data['username'] == login_username and profile_data['password'] == login_password:
                        logging.debug("log in successfull")
                        return_value = True
                        profile_data['validity'] = True
                        self.m_ProfileInfo.update(profile_data)
                        page_to_open = './html/homepage.html'
                    elif profile_data['username'] != login_username:
                        return_value = True
                        logging.debug('User does not exist. Please register.')
                        set_error_status = 'User does not exist. Please register.'
                        page_to_open = './html/index.html'
                    else:
                        return_value = True
                        logging.debug("Invalid password")
                        set_error_status = 'Invalid password. Try again.'
                        page_to_open = './html/index.html'
                else:
                    logging.debug("Unable to access data base")
                    page_to_open = './html/index.html'
                    return_value = False

                file_content = open(page_to_open).read()
                if set_error_status is not None:
                    file_content = file_content.replace('<!-- LOGIN_STATUS -->', '<b>' + set_error_status + '</b>')
            except OSError:
                return_value = False
                logging.error("Unable to open file")
        else:
            try:
                page_to_open = './html/index.html'
                file_content = open(page_to_open).read()
                return_value = True
            except OSError:
                logging.error("Unable to open file")
                file_content = []

        SessionManager.UpdateSession(self.m_SessionId, self.m_ProfileInfo)
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

    def GetParameterSet(self, session_id: uuid, param_set: dict):
        """extract parameter set and store it

        :param session_id:
        :type uuid
        :param param_set: dictionary containing all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        super().GetParameterSet(session_id, param_set)

    def CreateResponse(self) -> Tuple[bool, str]:
        """create html response

        :return: status, html content
        :rtype: boolean, string

        """
        file_content = []
        if b'signup_usernameid' not in self.m_ParameterSet or b'signup_passwordid' not in self.m_ParameterSet or b'signup_emailid' not in self.m_ParameterSet:
            logging.error('Username or password undefined')
            self.m_ProfileInfo['validate'] = False
            error_message = None
            if b'signup_usernameid' not in self.m_ParameterSet:
                error_message = 'Please enter a valid user name.'
            elif b'signup_passwordid' not in self.m_ParameterSet:
                error_message = 'Please enter a password.'
            else:
                error_message = 'Please enter an email address.'

            page_to_open = './html/index.html'
            try:
                file_content = open(page_to_open).read()
                file_content = file_content.replace('<!-- LOGIN_STATUS -->', '<b>' + error_message + '</b>')
                return_value = True
            except OSError:
                logging.error("Unable to open file")
                return_value = False
                file_content = []
        else:
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

            return_value = self.m_UserAccessInterface.read(profile_data)
            if return_value:
                if signup_username != profile_data['username']:
                    profile_data['username'] = signup_username
                    profile_data['password'] = signup_password
                    profile_data['email'] = signup_email
                    return_value = self.m_UserAccessInterface.write(profile_data)
                    if return_value:
                        profile_dictionary['validity'] = True
                        username = profile_data['username']
                        password = profile_data['password']
                        email = profile_data['email']
                        return_value, file_content = ProfileHandler.Update(username, password, email)
                        if not return_value:
                            logging.error("Unable to open file")
                            return_value = False
                            file_content = []
                    else:
                        logging.error("Unable to access data base")
                        return_value = False
                        file_content = []

                    self.m_ProfileInfo.update(profile_dictionary)
                else:
                    logging.error('User already exist')
                    return_value = True
                    self.m_ProfileInfo.update(profile_data)
                    try:
                        file_content = open('./html/index.html').read()
                        file_content = file_content.replace('<!-- LOGIN_STATUS -->', 'Username is already registered. '
                                                                                     'Use a different user name.')
                    except OSError:
                        logging.error("Unable to open file")
                        return_value = False
                        file_content = []
            else:
                logging.error("Unable to access data base - user table")
                self.m_ProfileInfo['validate'] = False
                page_to_open = './html/index.html'
                try:
                    file_content = open(page_to_open).read()
                    file_content = file_content.replace('<!-- LOGIN_STATUS -->', 'Unable to establish connection to '
                                                                                 'database.')
                    return_value = True
                except OSError:
                    logging.error("Unable to open file")
                    return_value = False
                    file_content = []

        SessionManager.UpdateSession(self.m_SessionId, self.m_ProfileInfo)
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

    @staticmethod
    def Update(username, password, email, userID) -> Tuple[bool, str]:
        """Update, fills out profile form

        :param username: username
        :type: string
        :param password: password
        :type: string
        :param email: email
        :type: string
        :return: return_value, html content
        :rtype: boolean, string

        """
        try:
            file_content = open('./html/profile.html').read()
            return_value = True
        except OSError:
            return_value = False
            file_content = []
            logging.error("Unable to open profile page")

        if return_value:
            details_list = str()
            table_row = ProfileHandler.m_HTMLTableRowDescriptor
            table_row = table_row.replace('USERNAME', username)
            table_row = table_row.replace('PASSWORD', password)
            table_row = table_row.replace('EMAIL', email)
            details_list = table_row

            table_header = ProfileHandler.m_HTMLHeaderLine
            table_header = table_header.replace('<!-- header_attachment_anchor -->', details_list)

            table = ProfileHandler.m_HTMLTableResponse
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

    def GetParameterSet(self, session_id: uuid, param_set: dict):
        """extract parameter set and store it

        :param session_id: unique session identifier
        :type: uuid
        :param param_set: dictionary containing all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        super().GetParameterSet(session_id, param_set)

    def CreateResponse(self) -> Tuple[bool, str]:
        """create html response

        :return: status, html content
        :rtype: boolean, string

        """
        file_content = []
        return_value = False
        if self.m_ProfileInfo['validity']:
            username = self.m_ProfileInfo['username']
            password = self.m_ProfileInfo['password']
            email = self.m_ProfileInfo['email']
            userID = self.m_ProfileInfo['userID']
            return_value, file_content = ProfileHandler.Update(username, password,email, userID)

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

    def GetParameterSet(self, session_id: uuid, param_set: dict):
        """extract parameter set and store it

        :param session_id: unique id representing the session
        :type uuid
        :param param_set: dictionary containing all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        super().GetParameterSet(session_id, param_set)

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

    def GetParameterSet(self, session_id: uuid, param_set: dict):
        """extract parameter set and store it

        :param session_id: unique id representing the session
        :type: uiid
        :param param_set: dictionary containing all parameters
        :type: dict
        :return: -
        :rtype: -

        """
        super().GetParameterSet(session_id, param_set)

    def CreateResponse(self) -> Tuple[bool, str]:
        """create html response

        :return: status, html content
        :rtype: boolean, string

        """
        logging.debug('CreateResponse of logout handler called')
        return False