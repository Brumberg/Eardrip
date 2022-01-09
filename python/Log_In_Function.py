import mysql.connector

# connects python to the database
db = mysql.connector.connect(
    host = "localhost" ,
    user = "root" ,
    passwd = "Root" ,
    database = "testdatabase"
    )
mycursor = db.cursor()

def login():

    login_username = ()
    login_password = ()

    # searches database for the username
    mycursor.execute("SELECT * FROM user WHERE username = '%s'" % login_username)
    real_login_username = mycursor.fetchone()

    if real_login_username == None:
        print("INVALID USERNAME")

    elif real_login_username[1] == login_password:
        print("SUCCESSFUL")

    else:
        print("INVALID PASSWORD")

    mycursor.reset()
login()