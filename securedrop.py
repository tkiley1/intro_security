#!/usr/bin/env python3
from login import *

commands = {'help':help_func, 'exit':exit_func}

login()

while True:
    cmd = input("securedrop>")
    if cmd in commands:
        commands[cmd]()
    else:
        print("Invalid Command")
