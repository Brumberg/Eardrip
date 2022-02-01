from datetime import datetime, timedelta
from threading import Thread, Event, Lock
import logging
import time
import uuid

class SessionManager:
    """Stores and restores session information/content

    """
    m_Session = {}
    SCHEDULER_CYCLIC_TIME = 30
    SESSION_TIMEOUT = 24
    m_Thread = None
    m_SessionLock = Lock()

    def __init__(self, *arguments):
        """Constructor, session handler initializer

        :return: -
        :rtype: -

        """

    def __del__(self):
        """Destructor

        :return: -
        :rtype: -

        """


    @classmethod
    def StartScheduer(cls):
        """start session working thread

         :return: -
         :rtype: -

         """
        cls.m_Thread = Thread(target=cls.CheckTimeOut, args=[], daemon=True).start()

    @classmethod
    def StopScheduer(cls):
        """terminate session working thread

         :return: -
         :rtype: -

         """
        if cls.m_Thread is not None:
            cls.m_Thread.stop()
            cls.m_Thread = None

    @classmethod
    def CheckTimeOut(cls):
        """Session worker thread that calls every SCHEDULER_CYCLIC_TIME sec the function
        RemoveUnusedConnections() to remove unused connections

        :return: -
        :rtype: -

        """
        while True:
            time.sleep(cls.SCHEDULER_CYCLIC_TIME)
            cls.RemoveUnusedConnections()

    @classmethod
    def RemoveUnusedConnections(cls):
        """Checks for connections that are abandoned for at least SESSION_TIMEOUT hours
        and removes them from the dictionary

        :return: -
        :rtype: -

        """
        with cls.m_SessionLock:
            if cls.m_Session:
                now = datetime.now()
                keys = []
                for i in cls.m_Session:
                    if now > cls.m_Session[i]['session_expiring_timestamp']:
                        keys.append(i)

                for i in keys:
                    logging.info('Deleting session: {}, user: {}'
                                 .format(i, cls.m_Session[i]['session_context']['username']))
                    cls.m_Session.pop(i, None)





    @classmethod
    def CreateUinqueSessionId(cls) -> uuid:
        """Create a unique session id

        :return session id: unique identifier for the session
        :rtype: uuid

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
    def OpenSession(cls, session_identifier=None, session_context=None) -> uuid:
        """Creates or restores a(n) (existing) session

        :param session_identifier: unique id identifying the session
        :type: uuid
        :param session_context: session context - used if session is created/discarded if session is already registered
        :type: str
        :return: session_id
        :rtype: uuid

        """

        if session_identifier is not None:
            session_handle = None
            time_change = timedelta(hours=cls.SESSION_TIMEOUT)
            session_info = dict()
            session_info['session_timestamp'] = datetime.now()
            session_info['session_expiring_timestamp'] = datetime.now()+time_change
            session_info['session_id'] = session_identifier
            with cls.m_SessionLock:
                if cls.m_Session:
                    if session_identifier in cls.m_Session.keys():
                        session_handle = cls.m_Session[session_identifier]

                if session_handle is None:
                    session_info['session_context'] = session_context
                    cls.m_Session[session_identifier] = session_info
                else:
                    session_handle['session_timestamp'] = session_info['session_timestamp']
                    session_handle['session_expiring_timestamp'] = session_info['session_expiring_timestamp']
                    session_handle['session_id'] = session_info['session_id']
        else:
            session_identifier = cls.CreateUinqueSessionId()
            session_info = dict()
            dateTimeObj = datetime.now()
            session_info['session_timestamp'] = dateTimeObj
            time_change = timedelta(hours=cls.SESSION_TIMEOUT)
            session_info['session_expiring_timestamp'] = datetime.now() + time_change
            session_info['session_id'] = session_identifier
            session_info['session_context'] = session_context
            with cls.m_SessionLock:
                cls.m_Session[session_identifier] = session_info

        return session_identifier

    @classmethod
    def CloseSession(cls, session_identifier: uuid):
        """closes the current session

        :param session_identifier: unique id identifying the session
        :type: uuid
        :return: -
        :rtype: -

        """

        if cls.m_Session:
            if session_identifier in cls.m_Session.keys():
                del cls.m_Session[session_identifier]

    @classmethod
    def UpdateSession(cls, session_identifier: uuid, session_context: str):
        """Updates session context

        :param session_identifier: unique id identifying the session
        :type: uuid
        :param session_context: context required for the session to continue properly
        :type: str
        :return: -
        :rtype: -

        """

        if cls.m_Session:
            if session_identifier in cls.m_Session.keys():
                cls.m_Session[session_identifier]['session_context'] = session_context

    @classmethod
    def GetSessionContext(cls, session_identifier: uuid):
        """Session Handler

        :param session_identifier: contains a unique handle representing the session
        :type: uuid
        :return: session's context
        :rtype: str

        """
        return_value = None
        if cls.m_Session:
            if session_identifier in cls.m_Session.keys():
                return_value = cls.m_Session[session_identifier]['session_context']

        return return_value