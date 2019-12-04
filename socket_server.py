#!/usr/bin/env python3

#from ev3dev2.sound import Sound

import subprocess
import sys
import socket

#sound = Sound()

print("Started the server...")
#sound.speak('I am ready')

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 56789              # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen(1)
    conn, addr = sock.accept()
    f = open("received.png", 'wb')
    with conn:
        #sound.speak("Success")
        print("Connected by", addr)
        while True:
            l = conn.recv(1024)
            while(l):
                f.write(l)
                l = conn.recv(1024)
        
            #if 'up' in data:
            #    sound.speak("Button was pressed")
        f.close()
            
