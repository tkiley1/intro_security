#!/usr/bin/env python3
import hashlib
import getpass
import os

#simple login system

def login():
    uname  = input("Enter your username: ")
    passw  = getpass.getpass("Password: ").encode('utf-8')
    passwh = hashlib.sha256(passw).hexdigest()
    chkpth = "./users/" + uname
    if os.path.exists(chkpth):
        f = open(chkpth + "/password", "r")
        cpasswh = f.read()
        if cpasswh == passwh:
            print("Welcome " + uname)
            return uname
    print("Authentication Failed.")
    return -1

def register():
    uname = input("Enter a new username: ")
    while os.path.exists("./users/" + uname):
        uname = input("Username taken.  Enter a new username: ")
    os.mkdir("./users/" + uname)
    passw = getpass.getpass("Enter a password: ").encode("utf-8")
    passwh = hashlib.sha256(passw).hexdigest()
    f = open("./users/" + uname + "/password", "w")
    f.write(passwh)
    return
    
    
register()
login()
