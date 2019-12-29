#!/usr/bin/env python
import signal
import sys
import serial


port = sys.argv[1]
baud = int(sys.argv[2])

s = serial.Serial(port, baud, timeout = 0.1)

def signal_handler(signal, frame):
	s.flush()
	s.close()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while 1:
	a = s.read(1024)
	sys.stdout.write(a)
	sys.stdout.flush()
