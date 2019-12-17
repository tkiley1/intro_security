#!/usr/bin/env python3
import hashlib
import getpass
import os, sys, time 
from mqtt import *

# Function for logging into the system.  Called first thing when securedrop.py is executed
def login():
    if not os.path.exists("./users/"):
        os.mkdir("./users/")
        register()
    #prompt user for credentials
    uname  = input("Enter your username: ")
    #get hashed password from user
    passwh  = hashlib.sha256(getpass.getpass("Password: ").encode('utf-8')).hexdigest()
    #passwh = hashlib.sha256(passw).hexdigest()
    #check directory for matching user
    chkpth = "./users/" + uname
    #if a matching user exists, compare password hash with stored password hash
    if os.path.exists(chkpth):
        f = open(chkpth + "/password", "r")
        cpasswh = f.read()
        f.close()
        f = open(chkpth + '/email', "r")
        email = f.read()
        if cpasswh == passwh:
            print("Welcome " + uname)
            return uname, email
    print("Authentication Failed.")
    return -1

# Function for registering a new user.  It will prompt them for a new username and then create a user directory structure for the new user.  Only called from
# inside the login function
def register():
    #prompt user for a username and email
    uname = input("Enter a new username: ")
    #make sure the username is unique
    while os.path.exists("./users/" + uname):
        uname = input("Username taken.  Enter a new username: ")
    #create directory for new user
    os.mkdir("./users/" + uname)
    os.mkdir("./users/" + uname + "/contacts")
    email = input("Enter your Email: ")
    f = open("./users/" + uname + "/email", "w")
    f.write(email)
    f.close()
    #get password and store hash
    passwh = hashlib.sha256(getpass.getpass("Enter a password: ").encode("utf-8")).hexdigest()
    #passwh = hashlib.sha256(passw).hexdigest()
    f = open("./users/" + uname + "/password", "w")
    f.write(passwh)
    f.close()
    return 

# Simple function to print out the command options
def help_func(uname):
    print("'add' -> Add a new contact\n'list' -> List all online contacts\n'send' -> Transfer file to contact\n'exit' -> Exit SecureDrop")
    return

# Exit function
def exit_func(uname):
    sys.exit(0)

# Function to add new contacts.  This is a one way add, and contacts will only appear in the list if the other person has added the user back.
def add_func(uname):
    fname = input("Enter Full Name: ")
    email = input("Enter Email Address: ")
    fname = fname.replace(' ', '\ ')
    if not os.path.exists("./users/" + uname + "/" + 'contacts' + '/' + fname):
        os.mkdir("./users/" + uname + "/" +'contacts' + '/' + fname)
        f = open("./users/" + uname + "/" + 'contacts'+ '/' + fname +'/'+ 'email.txt', "w")
        f.write(email)
        f.close()
    else:
        os.remove("./users/" + uname + "/" + 'contacts'+ '/' + fname +'/'+ 'email.txt')
        f = open("./users/" + uname + "/" + 'contacts'+ '/' + fname +'/'+ 'email.txt', "w")
        f.write(email)
        f.close()
    print('Contact Added.')

# Function to list currently online contacts.
def list_func(mqttc,email,uname):
    global open_comms
    contacts = get_contacts(uname)
    for i in contacts:
        open_comms = open_comms + [i]
        message = bytearray("Sender<" + uname + "> CODE[100]", "UTF-8")
        message.extend(b'\0'*(150-len(message)))
        publish(mqttc, message)
    print("Polling for online contacts")
    return 0

# Function to send a file to a contact.
def send_func(uname):
    return 0

#Helper function to collect a users contacts
def get_contacts(uname):
    contact_list = []
    for d, n, f in os.walk("./users/" + uname + "/" +'contacts' + '/'):
        if os.path.exists(d + '/email.txt'):
            f = open(d + '/email.txt', "r")
            ctc = f.read()
            contact_list = contact_list + [ctc]
    return(contact_list)

#test ping function - currently unused
def tping(hostname):
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        print("Host up")
        return 0
    else:
        print("Host down")
        return 1
