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
def trackdata():
    #mycursor.execute("CREATE TABLE trackdata (artistid VARCHAR(50), (titleid VARCHAR(50), (trackid VARCHAR(50), (genreid VARCHAR(50), (popularity VARCHAR(50) (danceability VARCHAR(50), (energy VARCHAR(50), (liveness VARCHAR(50), (mode VARCHAR(50), (timesignature VARCHAR(50), (tempo VARCHAR(50), (valence VARCHAR(50), trackID int PRIMARY KEY AUTO_INCREMENT)")
    TRACK = ("abc")
    ARTIST = ("jeff bezos")
    TITLE = ("blabla")
    GENRE = ("REGGAE")
    POPULARITY = ("1")
    DANCEABILITY = ("2")
    ENERGY = ("2")
    KEY = ("A minor")
    LOUDNESS = ("6 LUFFS")
    MODE = ("something")
    SPEECHINESS = ("aax")
    ACOUSTICNESS = ("gg")
    INSTRUMENTALNESS = ("11")
    LIVENESS = ("3")
    VALENCE = ("idk")
    TEMPO = ("fast")
    TYPE = ("aa")
    ID = ("bb")
    URI= ("cc")
    HREF = ("dd")
    URL = ("ee")
    MS = ("ff")
    TIMESIGNATURE = ("140")

    mycursor.execute ("INSERT INTO trackdata (field_track_id, field_artist_id, field_title_id, field_genre_id, field_popularity, field_danceability, field_energy, field_key, field_loudness, field_mode, field_speechiness, field_acousticness, field_instrumentalness, field_liveness, field_valence, field_tempo, field_type, field_id, field_uri, field_track_href, field_analysis_url, field_duration_ms, field_time_signature) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (TRACK, ARTIST, TITLE, GENRE, POPULARITY, DANCEABILITY, ENERGY, KEY, LOUDNESS, MODE, SPEECHINESS, ACOUSTICNESS, INSTRUMENTALNESS, LIVENESS, VALENCE, TEMPO, TYPE, ID, URI, HREF, URL, MS, TIMESIGNATURE))
    db.commit()

songname = ("hello")

mycursor.execute("SELECT * FROM trackdata WHERE field_title_id = '%s'" % songname)
trackinfo = mycursor.fetchone()

trackinfo = ', '.join(trackinfo)
print(trackinfo)