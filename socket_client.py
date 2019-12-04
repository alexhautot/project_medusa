#!/usr/bin/env python3
from ev3dev.ev3 import *
from ev3dev2.sound import Sound
from ev3dev2.button import Button
#from time import sleep
#from threading import Thread
#import random
#import sys
import socket

sound = Sound()
button = Button()

# Echo client program

print('Started the client...')
sound.speak('Ok')

HOST = '192.168.43.71'    # The remote host
PORT = 56789              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    f = open("blue_prints.png",'rb') #open in binary
    l = f.read(1024)
    while l:
        sock.sendall(l)
        l = f.read(1024)

sock.close()
print('Received')
sound.speak("Confirmation message received")

