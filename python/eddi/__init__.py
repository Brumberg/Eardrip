from abc import ABCMeta, abstractmethod
from typing import Tuple
import mysql.connector


class IUserProfile:
    def __init__(self):
        """Constructor of interface

        :return: -
        :rtype: -

        """
        pass

    def __del__(self):
        """Destructor of interface

        :return: -
        :rtype: -

        """
        pass

    @abstractmethod
    def read(self, param_set: dict) -> bool:
        """function prototype to read user data/profile

        :param param_set:
        :param dict: object containing user profile
        :type: dict object
        :return: error/success
        :rtype: boolean

        """
        pass

    @abstractmethod
    def write(self, param_set: dict) -> bool:
        """function prototype to read user data/profile

        :param param_set:
        :param dict: object containing user profile
        :type: dict object
        :return: error/success
        :rtype: boolean

        """
        pass


class ITrackAttributes:
    def __init__(self):
        """Constructor of interface

        :return: -
        :rtype: -

        """
        pass

    def __del__(self):
        """Destructor of interface

        :return: -
        :rtype: -

        """
        pass

    @abstractmethod
    def read(self, param_set: dict) -> bool:
        """function prototype to read track attributes

        :param param_set:
        :param dict: object containing user profile
        :type: dict object
        :return: error/success
        :rtype: boolean

        """
        pass

    @abstractmethod
    def write(self, param_set: dict) -> bool:
        """function prototype to write track attributes

        :param param_set:
        :param dict: object containing user profile
        :type: dict object
        :return: error/success
        :rtype: boolean

        """
        pass


class Eddi:
    """Handles data base access
    Wraps all calls to and from the database (EardDipDatabaseInterface)
    responding to the request by updating/reloading the html page
    """
    m_DataBase = None
    m_UserProfile = None
    m_TrackProfile = None

    def __init__(self):
        """Constructor, resets the form handler dictionary

        :return: -
        :rtype: -

        """
        self.m_DataBase = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Root",
            database="eardrip_users"
        )

        self.m_UserProfile = Eddi.UserProfile(self)
        self.m_TrackProfile = Eddi.TrackAttributes(self)

    def __del__(self):
        """Destructor, cleanup of ressources

        :return: -
        :rtype: -

        """
        self.m_DataBase.close()

    def GetUserAccessInterface(self) -> IUserProfile:
        """returns interface to access user data

        :return: -
        :rtype: -

        """
        return self.m_UserProfile

    def GetTrackAttributesAccessInterface(self) -> ITrackAttributes:
        """returns interface to access track attributes

        :return: -
        :rtype: -

        """
        return self.m_TrackProfile

    class TrackAttributes(ITrackAttributes):
        """Handles profile data
        """
        m_Parent = None

        """Handles data base access for the profile
        Wraps all calls to and from the database (EarDripDatabaseInterface)
        responding to the request by updating/reloading the html page
        """

        def __init__(self, parent):
            """Constructor, resets the form handler dictionary

            :return: -
            :rtype: -

            """
            self.m_Parent = parent

        def __del__(self):
            """Destructor, releases resources

            :return: -
            :rtype: -

            """
            pass

        def read(self, param_set: dict) -> bool:
            """todo: add code to handle read request

            :param param_set:
            :param dict: object containing user profile
            :type: dict object
            :return: error/success
            :rtype: boolean

            """
            return False

        def write(self, param_set: dict) -> bool:
            """todo: add code to handle write request

            :param param_set:
            :param dict: object containing user profile
            :type: dict object
            :return: error/success
            :rtype: boolean

            """
            return_value = False
            try:
                cursor = self.m_Parent.m_DataBase.cursor()
                key_string = ','.join(param_set.keys())
                val_string = ','.join(param_set.values())

                #qry = "INSERT INTO trackdata (%s) Values (%s)" % (key_string, val_string)
                qry = "INSERT INTO trackdata (field_track_id, field_artist_id, field_title_id, field_genre_id, field_popularity, field_danceability, field_energy, field_key, field_loudness, field_mode, field_speechiness, field_acousticness, field_instrumentalness, field_liveness, field_valence, field_tempo, field_type, field_id, field_uri, field_track_href, field_analysis_url, field_duration_ms, field_time_signature) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (TRACK, ARTIST, TITLE, GENRE, POPULARITY, DANCEABILITY, ENERGY, KEY, LOUDNESS, MODE, SPEECHINESS, ACOUSTICNESS, INSTRUMENTALNESS, LIVENESS, VALENCE, TEMPO, TYPE, ID, URI, HREF, URL, MS, TIMESIGNATURE)

                cursor.execute(qry, param_set.keys() + param_set.values())
                self.m_Parent.m_DataBase.commit()
                cursor.close()
                return_value = True
            except:
                return_value = False

            return return_value

    class UserProfile(IUserProfile):
        """Handles profile data
        """
        m_Parent = None

        """Handles data base access for the profile
        Wraps all calls to and from the database (EarDripDatabaseInterface)
        responding to the request by updating/reloading the html page
        """

        def __init__(self, parent):
            """Constructor, resets the form handler dictionary

            :return: -
            :rtype: -

            """
            self.m_Parent = parent

        def __del__(self):
            """Destructor, releases resources

            :return: -
            :rtype: -

            """
            pass

        def read(self, param_set: dict) -> bool:
            """todo: add code to handle read request

            :param param_set:
            :param dict: object containing user profile
            :type: dict object
            :return: error/success
            :rtype: boolean

            """
            return_value = True
            try:
                cursor = self.m_Parent.m_DataBase.cursor()
                cursor.execute("SELECT username FROM user WHERE username = '%s'" % dict['username'])
                real_login_username = cursor.fetchone()
                cursor.reset()
                cursor.execute("SELECT password FROM user WHERE username = '%s'" % dict['username'])
                real_login_password = cursor.fetchone()
                cursor.reset()
                cursor.execute("SELECT email FROM user WHERE username = '%s'" % dict['username'])
                real_login_email = cursor.fetchone()
                cursor.close()
                dict['username'] = real_login_username
                dict['password'] = real_login_password
                dict['email'] = real_login_email
            except:
                return_value = False
            return return_value


        def write(self, param_set: dict) -> bool:
            """todo: add code to handle write request

            :param param_set:
            :param dict: object containing user profile
            :type: dict object
            :return: error/success
            :rtype: boolean

            """
            return_value = True
            try:
                cursor = self.m_Parent.m_DataBase.cursor()
                cursor.execute("INSERT INTO user (username, password, email) VALUES (%s, %s, %s)", (dict['username'], dict['password'], dict['email']))
                self.m_Parent.m_DataBase.commit()
            except:
                return_value = False
            cursor.close()
            return return_value

