from PYTHON.Log_In_Function import *

LoggedIn = False
ValidInput = False

# user can decide if they want to continue or go back to homepage
def logout():
    while ValidInput == False:
        userinput = input ("""Enter "YES" if you wish to continue to log out or "NO" to go back to main page: """)
        if userinput == ("YES"):
            print ("Logged Out")
            LoggedIn == False
            ValidInput == True
            quit()

        elif userinput == ("NO"):
            LoggedIn == True
            homepage()
        else:
            print ("Please enter a valid input: ")
            ValidInput == False
