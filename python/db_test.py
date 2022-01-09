import mysql.connector

# connects python to the database
db = mysql.connector.connect(
    host = "localhost" ,
    user = "root" ,
    passwd = "Root" ,
    database = "testdatabase"
    )
mycursor = db.cursor()

# creates a database
def createdatabase():
    mycursor.execute("CREATE DATABASE testdatabase")


# creates a table
def createtable():
    mycursor.execute("CREATE TABLE user (username VARCHAR(50), password VARCHAR(50), email VARCHAR(50), userID int PRIMARY KEY AUTO_INCREMENT)")


# adds data to the table
def commit():
    mycursor.execute ("INSERT INTO user (username, password, email) VALUES (%s, %s, %s)", (username, password, useremail))
    db.commit()


# displays database content
def displaycontent():
    mycursor.execute ("SELECT * FROM user")
    for x in mycursor:
        print (x)


# searches the password that corresponds with the username
def searchconditionally():
    userinput = ("12345")

    username1 = ("sam cliffe")

    mycursor.execute("SELECT password FROM user WHERE username = '%s'" % username1)
    realpassword = mycursor.fetchone()

    realpassword = ''.join(realpassword)

def generalsearch():
    usernameinput = input ("ENTER USERNAME: ")

    mycursor.execute("SELECT username FROM user WHERE username = '%s'" % usernameinput)
    realusername = mycursor.fetchone()

    if realusername == (None):
        print("USERNAME DOESNT EXIST")

    else:
        realusername = ''.join(realusername)
        print("WELCOME, " + usernameinput)

displaycontent()