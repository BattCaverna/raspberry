#!/usr/bin/env python
import socket
import binascii

TCP_IP = 'battcaverna.local'
TCP_PORT = 2020
BUFFER_SIZE = 128
MESSAGE = "\x10\x03\x00\x02\x00\x01\x26\x8b"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.settimeout(1)
error = 0
pkt = 0
while 1:
    s.send(MESSAGE)
    data = s.recv(BUFFER_SIZE)
    pkt += 1
    if binascii.hexlify(data) != "100302005ec5bf":
        error += 1

    if pkt % 1000 == 0:
        print "pkt error %d/%d (%.1f%%)" % (error, pkt, error * 100.0 / pkt)
  
s.close()
