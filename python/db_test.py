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
    mycursor.execute("CREATE TABLE user (username VARCHAR(50), password VARCHAR(50), email VARCHAR(50), userID int PRIMARY KEY AUTO_INCREMENT)")

    # mysql trackdata create table function
    # CREATE TABLE trackdata (field_track_id VARCHAR (250), field_artist_id VARCHAR (250), field_title_id VARCHAR (250), field_genre_id VARCHAR (250), field_popularity VARCHAR (250), field_danceability VARCHAR (250), field_energy VARCHAR (250), field_key VARCHAR (250), field_loudness VARCHAR (250), field_mode VARCHAR (250), field_speechiness VARCHAR (250), field_acousticness VARCHAR (250), field_instrumentalness VARCHAR (250), field_liveness VARCHAR (250), field_valence VARCHAR (250), field_tempo VARCHAR (250), field_type VARCHAR (250), field_id VARCHAR (250), field_uri VARCHAR (250), field_track_href VARCHAR (250), field_analysis_url VARCHAR (250), field_duration_ms VARCHAR (250), field_time_signature VARCHAR (250), tlike VARCHAR (250), userID INT, CONSTRAINT userID FOREIGN KEY (userID) REFERENCES user (userID) ON UPDATE CASCADE ON DELETE CASCADE);

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
    mycursor.execute("DELETE FROM trackdata")
    db.commit()

# searches the password that corresponds with the username
def searchconditionally():
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
