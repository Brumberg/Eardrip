
import mysql.connector
from mysql.connector import errorcode

class dubpy
    ## database name
    m_HostName = 'localhost'
    m_UserName = 'root'
    m_UserPassword = 'Root'
    m_DataBaseName = 'testdatabase'
    m_DataBaseStatus = False
    m_DataBaseExists = False
    m_DataBaseHandler = []
    m_Cursor = []

    def __init__(self, hostname='localhost', username='root', userpassword='Root', databasename='testdatabase'):
        self.m_HostName = hostname
        self.m_UserName = username
        self.m_UserPassword = userpassword
        self.m_DataBaseName = databasename
        self.m_DataBaseStatus = True
        try:
            self.m_DataBaseHandler = mysql.connector.connect(
                host=self.m_HostName,
                user=self.m_UserName,
                passwd=self.m_UserPassword,
            )
            self.m_Cursor = self.m_DataBaseHandler .cursor()
        except mysql.connector.Error as err:
            self.m_DataBaseStatus = True
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('Database does not exist')
            else:
                print(err)

        if self.m_DataBaseStatus:
            try:
                self.m_Cursor.execute("USE {}".format(self.m_DataBaseName))
                self.m_DataBaseExists = True
            except mysql.connector.Error as err:
                print("Database {} does not exists.".format(self.m_DataBaseName))

    def _del__(self):
        if self.m_DataBaseStatus!=False:
            self.m_DataBaseHandler.close()
            self.m_Cursor.close()
            self.m_DataBaseStatus = False
            self.m_DataBaseExists = False


    def CreateDataBase(self):
        if  self.m_DataBaseStatus == True:
            try:
                self.m_Cursor.execute(
                    "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.m_DataBaseName))
            except mysql.connector.Error as err:
                print("Failed creating database: {}".format(err))

            if self.m_DataBaseStatus:
                self.m_Cursor.execute('CREATE DATABASE {}'.format(self.m_DataBaseName))
            else:
                print('Database does not exist.')

            try:
                self.m_Cursor.execute("USE {}".format(self.m_DataBaseName))
                self.m_DataBaseExists = True
            except mysql.connector.Error as err:
                print("Database {} does not exists.".format(self.m_DataBaseName))
                self.m_DataBaseExists = False
        else:
            print('Database does not exist.')

    def CreateTable(self, name, table):
        self.m_Cursor.execute("CREATE TABLE user (username VARCHAR(50), password VARCHAR(50), email VARCHAR(50), userID int PRIMARY KEY AUTO_INCREMENT)")

    def displaycontent(filter, table):
        self.m_Cursor.execute("SELECT {} FROM {}".format(filter, table))
        for x in mycursor:
            print(x)

    def search(filter, tablename, itemname):
        self.m_Cursor.execute("SELECT '%s' FROM %s WHERE %s = '%s'" %filter, % tablename, % itemname)
        return  self.m_Cursor.fetchone()