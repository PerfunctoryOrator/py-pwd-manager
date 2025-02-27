#
#  Password Manager.py
#
#  Created by Yashdeep Singh Fauzdar on 02/12/24.
#

# Import required modules
from datetime import datetime, timezone
from os import mkdir, path # To make the program multi-OS compatible
from pickle import dump, load
from platform import system
from random import choice
from time import sleep

# Reset the database file
def resetDbFile():
    with open(filePath, "wb") as dbFile:
        dump({}, dbFile)
    with open(filePath, "ab") as dbFile:
        dump({}, dbFile)

def getRandomCharacter(group = 4):

    # Define different character sets
    characters = [
        ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
        ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"],
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
        ["~", "!", "@", "#", "$", "%", "&", "*", "(", ")", "-", "_", "=", "+", "[", "]", "|", ";", ":", "'", ",", "<", ".", ">", "/", "?"]
    ]

    randomCharacterSet = []
    if group == 4: # `4` is the default value for `group`; choose any random character set to select the character from
        randomCharacterSet = characters[choice(range(4))]
    else:
        randomCharacterSet = characters[group]

    # Get and return a random character from the chosen set as a letter for the password
    return(randomCharacterSet[choice(range(len(randomCharacterSet)))])

# Get and return the date and time (in IST — GMT+5:30)
def getDateTime():

    monthNames = ["nil", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    nowGMT = datetime.now(timezone.utc)
    dayIST = int(nowGMT.strftime("%d"))
    monthIST = int(nowGMT.strftime("%m"))
    yearIST = int(nowGMT.strftime("%Y"))

    daysInMonth = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if yearIST % 4 == 0:
        if yearIST % 100 == 0:
            if yearIST % 400 == 0:
                daysInMonth[2] = 29
        else:
            daysInMonth[2] = 29

    hourIST = int(nowGMT.strftime("%H")) + 5
    minuteIST = int(nowGMT.strftime("%M")) + 30
    if minuteIST > 59:
        minuteIST -= 60
        hourIST += 1
    if hourIST > 23:
        hourIST -= 24
        dayIST += 1
    if dayIST > daysInMonth[monthIST]:
        dayIST -= daysInMonth[monthIST]
        monthIST += 1
    if monthIST > 12:
        monthIST -= 12
        yearIST += 1

    if hourIST > 12:
        time = f"{str(hourIST - 12)}:{str(minuteIST)}:{nowGMT.strftime('%S')} PM"
    else:
        time = f"{str(hourIST)}:{str(minuteIST)}:{nowGMT.strftime('%S')} AM"

    return(f"on {dayIST} {monthNames[monthIST]} {yearIST} at {time}")

def printPasswordsAsTable(data):

    # Define important variables for printing the table
    headerLabels = ["Serial No.", "Keyword", "Password", "Last Updated"]
    noOfHeaders = len(headerLabels)
    passwordInfo = data
    noOfPasswords = len(passwordInfo)
    border = ""
    widthOfColumns = [0] * noOfHeaders

    # Get the width of all the columns of the table
    for row in range(noOfPasswords):
        for column in range(noOfHeaders - 1):# To compensate for missing `Serial No.` column in passwordInfo[row]
            if len(passwordInfo[row][column]) > widthOfColumns[column + 1]:
                widthOfColumns[column + 1] = len(passwordInfo[row][column])
    for column in range(noOfHeaders):
        if len(headerLabels[column]) > widthOfColumns[column]:
            widthOfColumns[column] = len(headerLabels[column])
    if len(str(noOfPasswords)) > widthOfColumns[0] - 1:
        widthOfColumns[0] = len(str(noOfPasswords)) + 1

    # Add serial numbers at the beginning of each row of the table
    for row in range(1, noOfPasswords + 1):
        passwordInfo[row - 1].insert(0, " " * (widthOfColumns[0] - 1 - len(str(row))) + str(row) + ".")

    # Define the row-separator as a string, eg. +------------+---------+----------+--------------+
    for column in range(noOfHeaders):
        border +=  "+" + "-" * (widthOfColumns[column] + 2)
    border += "+"

    # Print the headers (column titles) for different columns of the table
    print(border)
    for column in range(noOfHeaders):
        print(f"| {headerLabels[column]}{' ' * (widthOfColumns[column] - len(headerLabels[column]))}", end = " ")
    print(f"|\n{border}")

    # Print the requested passwords along with all their information in the form of a table
    for row in range(noOfPasswords):
        for column in range(noOfHeaders):
            print(f"| {passwordInfo[row][column]}{' ' * (widthOfColumns[column] - len(passwordInfo[row][column]))}", end = " ")
        print("|")
    print(border)

# Define variables
filePath = ""
dbFile = None

# Set up the database folder (hidden) on various systems
if system() == "Darwin": # On macOS
    filePath = path.expanduser("~/Library/Application Support/pwdmanagerpy")
    if not path.exists(filePath):
        mkdir(filePath)
    filePath = path.expanduser("~/Library/Application Support/pwdmanagerpy/passwords.db")
elif system() == "Linux": # On Linux distros
    filePath = path.expanduser("~/.pwdmanagerpy")
    if not path.exists(filePath):
        mkdir(filePath)
    filePath = path.expanduser("~/.pwdmanagerpy/passwords.db")
elif system() == "Windows": # On Windows
    filePath = path.expanduser(r"~\AppData\Roaming\pwdmanagerpy")
    if not path.exists(filePath):
        mkdir(filePath)
    filePath = path.expanduser(r"~\AppData\Roaming\pwdmanagerpy\passwords.db")
else: # Some other OS
    filePath = "passwords.db" # Save the database alongside the program in a file visible to the user
    print("\n\n\nIf you wish to move this program to another location, you must carry the ‘passwords.db’ file along with this to the new location, otherwise all your saved passwords will get lost.")

# Set up the database file inside the database folder
if not path.exists(filePath):
    resetDbFile()
else:
    try:
        with open(filePath, "rb") as dbFile:
            load(dbFile)
            load(dbFile)
    except EOFError:
        resetDbFile()

# Run the program in an endless loop so that the user doesn’t have to start it repeatedly
while True:

    # Define variables
    i = lengthOfPassword = 0
    userChoice = passwordKey = password = ""
    passwordInfo = []
    db1 = {} # `db1` stores [passwordKey: password]
    db2 = {} # `db2` stores [passwordKey: lastModified]

    # Show menu and ask for input from the user
    print("\n\nWhat do you want to do?\n\n1. Generate Password\n2. Save Password\n3. Update Password\n4. View Password\n5. Delete Password\n6. Quit\n")
    userChoice = input("Enter your choice: ")
    while not userChoice.isdigit() or int(userChoice) < 1 or int(userChoice) > 6: # The user entered unsupported value as their choice
        userChoice = input("Please select from 1 to 6: ")

    # Get password data from database (in advance)
    with open(filePath, "rb") as dbFile:
        db1 = load(dbFile)
        db2 = load(dbFile)

    if userChoice == "1": # Generate Password

        # Ask the length of the password to be generated
        lengthOfPassword = input("\n\nEnter the length of the password that you want to create (a whole number between 8 and 32): ")
        while not lengthOfPassword.isdigit() or int(lengthOfPassword) < 8 or int(lengthOfPassword) > 32:
            lengthOfPassword = input("The length of the password must be a whole number between between 8 and 32; please enter another value: ")
        lengthOfPassword = int(lengthOfPassword)

        # Generate password
        print("\nGenerating Password…", end = "")
        sleep(1)
        password += getRandomCharacter(group = 0)
        password += getRandomCharacter(group = 1)
        password += getRandomCharacter(group = 2)
        password += getRandomCharacter(group = 3)
        for i in range(lengthOfPassword - 4):
            password += getRandomCharacter()

        # Show generated password
        print(f"\n\nThe generated password is: {password}", end = "")
        sleep(1)

        # Ask to save password
        userChoice = input("\n\nDo you want to save this password? [Yes / No] ")

        # Proceed to save password
        if userChoice.lower() == "yes" or userChoice.lower() == "y":

            # Ask for keyword
            passwordKey = input("Enter a unique keyword with which you can identify your password later: ")
            while passwordKey == "all" or passwordKey in db1:
                if passwordKey == "all":
                    passwordKey = input("The keyword can’t be ‘all’; please enter another keyword: ")
                else:
                    passwordKey = input("A password has already been saved with this keyword; please enter another keyword: ")

            # Save the password to database
            db1.update({passwordKey: password})
            db2.update({passwordKey: getDateTime()})
            with open(filePath, "wb") as dbFile:
                dump(db1, dbFile)
            with open(filePath, "ab") as dbFile:
                dump(db2, dbFile)
            print("\nPassword saved successfully.")

    elif userChoice == "2": # Save Password

        # Ask for password and keyword
        password = input("\n\nEnter the password that you want to save: ")
        passwordKey = input("Enter a unique keyword with which you can identify your password later: ")
        while passwordKey == "all" or passwordKey in db1:
            if passwordKey == "all":
                passwordKey = input("The keyword can’t be ‘all’; please enter another keyword: ")
            else:
                passwordKey = input("A password has already been saved with this keyword; please enter another keyword: ")

        # Save the password to database
        db1.update({passwordKey: password})
        db2.update({passwordKey: getDateTime()})
        with open(filePath, "wb") as dbFile:
            dump(db1, dbFile)
        with open(filePath, "ab") as dbFile:
            dump(db2, dbFile)
        print("\nPassword saved successfully.")

    elif userChoice == "3": # Update Password

        if len(db1) == 0:
            print("\n\nNo password has been saved.")
        else:

            # Format and add all the data to `passwordInfo`
            for i in db1:
                passwordInfo.append([i, db1[i], ""])
            userChoice = 0
            for i in db2:
                passwordInfo[userChoice][2] = db2[i]
                userChoice += 1

            # Show all passwords
            print("\n")
            printPasswordsAsTable(passwordInfo)

            # Ask which password to update
            userChoice = input("\n\nEnter the keyword for the password that you want to update: ")

            if userChoice in db1:

                # Update the password
                password = input(f"Enter a new password for the keyword ‘{userChoice}’: ")
                db1[userChoice] = password
                db2[userChoice] = getDateTime()
                with open(filePath, "wb") as dbFile:
                    dump(db1, dbFile)
                with open(filePath, "ab") as dbFile:
                    dump(db2, dbFile)
                print("\nPassword updated successfully.")

            else:
                print("\nNo password has been saved with this keyword.")

    elif userChoice == "4": # View Password

        if len(db1) == 0:
            print("\n\nNo password has been saved.")
        else:

            # Ask user the keyword for the password that they want to view
            userChoice = input("\n\nEnter the keyword for the password that you want to view (enter ‘all’ if you want to view all the passwords): ")

            if userChoice == "all":

                # Format and add all the data to `passwordInfo`
                for i in db1:
                    passwordInfo.append([i, db1[i], ""])
                userChoice = 0
                for i in db2:
                    passwordInfo[userChoice][2] = db2[i]
                    userChoice += 1

                print()
                printPasswordsAsTable(passwordInfo)

            elif userChoice in db1:
                print()

                printPasswordsAsTable([[userChoice, db1[userChoice], db2[userChoice]]])
            else:
                print("\nNo password has been saved with this keyword.")

    elif userChoice == "5": # Delete Password

        if len(db1) == 0:
            print("\n\nNo password has been saved.")
        else:
            # Format and add all the data to `passwordInfo`
            for i in db1:
                passwordInfo.append([i, db1[i], ""])
            userChoice = 0
            for i in db2:
                passwordInfo[userChoice][2] = db2[i]
                userChoice += 1

            # Show all passwords
            print("\n")
            printPasswordsAsTable(passwordInfo)

            # Ask which password to delete
            userChoice = input("\n\nEnter the keyword for the password that you want to delete (enter ‘all’ if you want to delete all the passwords): ")

            if userChoice == "all": # Delete all passwords
                resetDbFile()
                print("\nPasswords deleted successfully.")

            elif userChoice in db1: # Delete a particular password

                del db1[userChoice]
                del db2[userChoice]

                with open(filePath, "wb") as dbFile:
                    dump(db1, dbFile)
                with open(filePath, "ab") as dbFile:
                    dump(db2, dbFile)

                print("\nPassword deleted successfully.")

            else:
                print("\nNo password has been saved with this keyword.")

    else: # Quit
        print("\n\n\n")
        break

    sleep(1)
