from PYTHON.Log_In_Function import *
from PYTHON.Log_Out_Function import *
from PYTHON.Sign_Up_Function import *

# the main homepage which gives the user different options they can choose from
def homepage():
    ValidInput = False
    print ("""---- HOMEPAGE ----
    1. Log In
    2. Sign Up
    3. Log Out""")

# ensures that the value that the user enters is correct and then redirects the user to the relevant option
    userinput = int(input("Please choose an option from above: "))
    while ValidInput == False:
        if userinput == (1):
            ValidInput = True
            login()

        elif userinput == (2):
            ValidInput = True
            signup()

        elif userinput == (3):
            ValidInput = True
            logout()

        else:
            print("Invalid Input")
            userinput = int(input("Please choose an option from above: "))

homepage()
