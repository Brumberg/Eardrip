from datetime import datetime, timedelta
import uuid

class SessionManager:

    m_Session = {}
    def __init__(self, *arguments):
        """Constructor, session handler initializer

        :return: -
        :rtype: -

        """
        print("Session manager instantiated")

    def __del__(self):
        """Destructor

        :return: -
        :rtype: -

        """
        print("Session manager deleted")

    @classmethod
    def CreateUinqueSessionId(cls):
        """Session Handler

        :return: -
        :rtype: -

        """
        unique_id = None
        if not cls.m_Session:
            unique_id = uuid.uuid1()  # or uuid.uuid4()
        else:
            unique_id = uuid.uuid1()  # or uuid.uuid4()
            while unique_id in cls.m_Session:
                unique_id = uuid.uuid1()  # or uuid.uuid4()
        return unique_id

    @classmethod
    def OpenSession(cls, session_identifier=None, session_context=None):
        """Session Handler

        :return: -
        :rtype: -

        """

        if session_identifier != None:
            session_handle = None
            if cls.m_Session:
                if session_identifier in cls.m_Session.keys():
                    session_handle = cls.m_Session[session_identifier]

            time_change = timedelta(hours=1)
            session_info = dict()
            session_info['session_timestamp'] = datetime.now()
            session_info['session_expiring_timestamp'] = datetime.now()+time_change
            session_info['session_id'] = session_identifier

            if session_handle == None:
                session_info['session_context'] = session_context
                print(session_context)

                cls.m_Session[session_identifier] = session_info
                print(cls.m_Session[session_identifier])
            else:
                session_handle['session_timestamp'] = session_info['session_timestamp']
                session_handle['session_expiring_timestamp'] = session_info['session_expiring_timestamp']
                session_handle['session_id'] = session_info['session_id']
        else:
            session_identifier = cls.CreateUinqueSessionId()
            session_info = dict()
            dateTimeObj = datetime.now()
            session_info['session_timestamp'] = dateTimeObj
            time_change = timedelta(hours=1)
            session_info['session_expiring_timestamp'] = datetime.now() + time_change
            session_info['session_id'] = session_identifier
            session_info['session_context'] = session_context
            cls.m_Session[session_identifier] = session_info

        return session_identifier

    @classmethod
    def CloseSession(cls, session_identifier):
        """Session Handler

        :return: -
        :rtype: -

        """

        if cls.m_Session:
            if session_identifier in cls.m_Session.keys():
                del cls.m_Session[session_identifier]

    @classmethod
    def UpdateSession(cls, session_identifier, session_context):
        """Session Handler

        :return: -
        :rtype: -

        """

        if cls.m_Session:
            if session_identifier in cls.m_Session.keys():
                cls.m_Session[session_identifier]['session_context'] = session_context

    @classmethod
    def GetSessionContext(cls, session_identifier):
        """Session Handler

        :return: -
        :rtype: -

        """
        return_value = None
        if cls.m_Session:
            if session_identifier in cls.m_Session.keys():
                return_value = cls.m_Session[session_identifier]['session_context']
        return return_value