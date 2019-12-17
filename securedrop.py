#!/usr/bin/env python3
from login import *
from mqtt import *
# Simple driver for the secure drop application.

commands = {'help':help_func, 'exit':exit_func, 'add':add_func, 'list':list_func, 'send':send_func, 'register':register}
uname, email = login()
if (uname) == -1:
	sys.exit(1)
mqttc = initialize(email)
print("press ctl + c to unlock console")
while True:
    try:
        listen(mqttc)
    except KeyboardInterrupt:
        cmd = input("securedrop>")
        if cmd in commands:
            if cmd == 'list':
                commands[cmd](mqttc, email, uname)
            elif cmd == 'register':
                commands[cmd]()
            else:
                commands[cmd](uname)
        else:
            print("Invalid Command")
        print("press ctl + c to unlock console")
