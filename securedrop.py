#!/usr/bin/env python3
from login import *

# Simple driver for the secure drop application.

commands = {'help':help_func, 'exit':exit_func, 'add':add_func, 'list':list_func, 'send':send_func}
uname = login()
if (uname) == -1:
	sys.exit(1)

while True:
    cmd = input("securedrop>")
    if cmd in commands:
        commands[cmd](uname)
    else:
        print("Invalid Command")
