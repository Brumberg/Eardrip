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
    mycursor.execute("DROP TABLE trackdata")

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
    mycursor.execute("DELETE * FROM user WHERE username='sam cliffe';")
    db.commit()

def deleteall():
    mycursor.execute("DELETE FROM trackdata")
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


# mysql code
#use eardrip_users;
#CREATE TABLE trackdata (field_track_id VARCHAR(128), field_artist_id VARCHAR(128), field_title_id VARCHAR(128), field_genre_id VARCHAR(128), field_popularity VARCHAR(20), field_danceability VARCHAR(20), field_energy VARCHAR(20), field_key VARCHAR(128), field_loudness VARCHAR(20), field_mode VARCHAR(20), field_speechiness VARCHAR(20), field_acousticness VARCHAR(20), field_instrumentalness VARCHAR(20), field_liveness VARCHAR(20), field_valence VARCHAR(20), field_tempo VARCHAR(20), field_type VARCHAR(20), field_id VARCHAR(128), field_uri VARCHAR(128), field_track_href VARCHAR(128), field_analysis_url VARCHAR(128), field_duration_ms VARCHAR(20), field_time_signature VARCHAR(50));
#INSERT INTO trackdata (field_track_id, field_artist_id, field_title_id, field_genre_id, field_popularity, field_danceability, field_energy, field_liveness, field_mode, field_time_signature, field_tempo, field_valence) Values ("2r6OAV3WsYtXuXjvJ1lIDi", "Pop Smoke_0", "Hello feat. A Boogie Wit da Hoodie", "brooklyn drill", "82", "DANCEABILITY", "ENERGY", "LIVENESS", "MODE", "TIME_SIGNATURE", "TEMPO", "VALENCE");

