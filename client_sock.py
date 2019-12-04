import socket
import sys
HOST = '192.168.43.71'

def send_file(file_name):
    s = socket.socket()
    s.connect((HOST,9999))
    f = open (file_name, "rb")
    l = f.read(1024)
    while (l):
        s.send(l)
        l = f.read(1024)
    s.close()

send_file("blue_prints.png")
