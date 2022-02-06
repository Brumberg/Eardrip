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
    def read(self, userID) -> (bool, [dict]):
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
    Wraps all calls to and from the database (EarDipDatabaseInterface)
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

        """Handles database access for the profile
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

        def read(self, userID) -> (bool, [dict]):
            """todo: add code to handle read request
            :param param_set:
            :param dict: object containing user profile
            :type: dict object
            :return: error/success
            :rtype: boolean

            """

            cursor = self.m_Parent.m_DataBase.cursor()

            cursor.execute("SELECT * FROM trackdata WHERE user_id = '%s'" % userID)
            selectedtracks = cursor.fetchall()
            selected_tracks_dictionary_list = []

            if selectedtracks == None:
                return False
            else:
                for x in selectedtracks:
                    dictionary = dict()
                    dictionary["ARTIST_ID"] = x[0]
                    dictionary["TITLE_ID"] = x[1]
                    dictionary["TRACK_ID"] = x[2]
                    dictionary["GENRE_ID"] = x[3]
                    dictionary["POPULARITY"] = x[4]
                    selected_tracks_dictionary_list.append(dictionary)
                cursor.reset()
            param_set = selected_tracks_dictionary_list
            return True, param_set
            # return dictionary instead of false

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
                qkeys = ', '.join(param_set.keys())
                qvalues = ', '.join("'%s'" % s for s in param_set.values())
                qry = "INSERT INTO trackdata (%s) VALUES (%s)" % (qkeys, qvalues)
                cursor.execute(qry)
                self.m_Parent.m_DataBase.commit()
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
                cursor.execute("SELECT username FROM user WHERE username = '%s'" % param_set['username'])
                real_login_username = cursor.fetchone()
                cursor.reset()
                cursor.execute("SELECT password FROM user WHERE username = '%s'" % param_set['username'])
                real_login_password = cursor.fetchone()
                cursor.reset()
                cursor.execute("SELECT email FROM user WHERE username = '%s'" % param_set['username'])
                real_login_email = cursor.fetchone()
                cursor.reset()
                cursor.execute("SELECT userID FROM user WHERE username = '%s'" % param_set['username'])
                username_tuple = cursor.fetchone()
                param_set ['userID'] = username_tuple[0]
                cursor.reset()
                if real_login_username is not None:
                    param_set['username'] = real_login_username[0]
                else:
                    param_set['username'] = ''

                if real_login_password is not None:
                    param_set['password'] = real_login_password[0]
                else:
                    param_set['password'] = ''

                if real_login_email is not None:
                    param_set['email'] = real_login_email[0]
                else:
                    param_set['email'] = ''
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
                cursor.execute("INSERT INTO user (username, password, email) VALUES (%s, %s, %s)", (param_set['username'], param_set['password'], param_set['email']))
                self.m_Parent.m_DataBase.commit()
            except:
                return_value = False

            return return_value

