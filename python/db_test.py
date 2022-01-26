import mysql.connector

# connects python to the database
db = mysql.connector.connect(
    host = "localhost" ,
    user = "root" ,
    passwd = "Root" ,
    database = "eardrip_users"
    )
mycursor = db.cursor()

# creates a database
def createdatabase():
    mycursor.execute("CREATE DATABASE eardrip_users")

# creates a table
def createtable():
    mycursor.execute("CREATE TABLE user_ (username VARCHAR(50), password VARCHAR(50), email VARCHAR(50), userID int PRIMARY KEY AUTO_INCREMENT)")

def deletetable():
    mycursor.execute("DROP TABLE users")

# adds data to the table
def commit():
    username = ("sam cliffe")
    password = ("12345")
    useremail = ("sam.j.cliffe@outlook.com")
    mycursor.execute ("INSERT INTO user (username, password, email) VALUES (%s, %s, %s)", (username, password, useremail))
    db.commit()


# displays database content
def displaycontent():
    mycursor.execute ("SELECT * FROM user")
    for x in mycursor:
        print (x)

# deletes database content
def delete():
    mycursor.execute("DELETE FROM user WHERE username='sam cliffe';")
    db.commit()

def deleteall():
    mycursor.execute("DELETE FROM user")
    db.commit()

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

#mycursor.execute("CREATE TABLE trackdata (artistid VARCHAR(50), (titleid VARCHAR(50), (trackid VARCHAR(50), (genreid VARCHAR(50), (popularity VARCHAR(50) (danceability VARCHAR(50), (energy VARCHAR(50), (liveness VARCHAR(50), (mode VARCHAR(50), (timesignature VARCHAR(50), (tempo VARCHAR(50), (valence VARCHAR(50), trackID int PRIMARY KEY AUTO_INCREMENT)")
