import mysql.connector

# connects python to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Root",
    database="testdatabase"
)
mycursor = db.cursor()


def signup():


    signup_username = ()
    signup_password = ()
    signup_email = ()

    # adds the variables to the user table in the database
    mycursor.execute("INSERT INTO user (username, password, email) VALUES (%s, %s, %s)", (signup_username, signup_password, signup_email))
    db.commit()
signup()