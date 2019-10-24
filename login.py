#!/usr/bin/env python3
import hashlib
import getpass
import os, sys, time 
import daemon, threading
import subprocess
#from mqtt import listen

#simple login system

def login():
    if not os.path.exists("./users/"):
        os.mkdir("./users/")
        register()
    #prompt user for credentials
    uname  = input("Enter your username: ")
    #get hashed password from user
    passw  = getpass.getpass("Password: ").encode('utf-8')
    passwh = hashlib.sha256(passw).hexdigest()
    #check directory for matching user
    chkpth = "./users/" + uname
    #if a matching user exists, compare password hash with stored password hash
    if os.path.exists(chkpth):
        f = open(chkpth + "/password", "r")
        cpasswh = f.read()
        if cpasswh == passwh:
            print("Welcome " + uname)
            return uname
    print("Authentication Failed.")
    return -1

def register():
    #prompt user for a username
    uname = input("Enter a new username: ")
    #make sure the username is unique
    while os.path.exists("./users/" + uname):
        uname = input("Username taken.  Enter a new username: ")
    #create directory for new user
    os.mkdir("./users/" + uname)
    #get password and store hash
    passw = getpass.getpass("Enter a password: ").encode("utf-8")
    passwh = hashlib.sha256(passw).hexdigest()
    f = open("./users/" + uname + "/password", "w")
    f.write(passwh)
    
    return

def help_func():
    print("'add' -> Add a new contact\n'list' -> List all online contacts\n'send' -> Transfer file to contact\n'exit' -> Exit SecureDrop")
    return

def exit_func():
    sys.exit(0)

#test ping function
def tping(hostname):
    #if = open("./tstout.txt")
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        print("Host up")
        return 0
    else:
        print("Host down")
        return 1
