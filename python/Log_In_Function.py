import mysql.connector

# connects python to the database
db = mysql.connector.connect(
    host = "localhost" ,
    user = "root" ,
    passwd = "Root" ,
    database = "testdatabase"
    )
mycursor = db.cursor()
LoggedIn = False

def login():
    validusername = False
    validpassword = False
    attempts = int(3)
    print("Welcome to the login page")

    # checks validity of username
    while validusername == False:
        usernameinput = input ("please enter your username: ")

        # searches database for the username
        mycursor.execute("SELECT username FROM user WHERE username = '%s'" % usernameinput)
        realusername = mycursor.fetchone()

        if realusername == (None):
            print("Invalid username, please try again")
            validusername = False

        else:
            realusername = ''.join(realusername)
            username = usernameinput
            validusername = True

    # checks validity of password + gives the user 3 attempts to get the password correct
    while validpassword == False:
        passwordinput = input ("please enter your password: ")

        # searches the for the username in the database and finds the corresponding password
        mycursor.execute("SELECT password FROM user WHERE username = '%s'" % username)
        realpassword = mycursor.fetchone()

        # converts the value from tuple form to string form
        realpassword = ''.join(realpassword)

        if passwordinput == (realpassword):
            validpassword = True
            print("welcome, "+username)
            LoggedIn = True

        else:
            print("Invalid password")
            attempts = (attempts - 1)
            if attempts == (0):
                print("you have 0 attempts left")
                quit()
            else:
                print("you have",attempts,"attempts left, please try again")
            validpassword = False