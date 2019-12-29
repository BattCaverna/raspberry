#!/bin/env python

import serial
import sys

port = sys.argv[1]
baud = int(sys.argv[2])

s = serial.Serial(port, baud)
s.rts = False
while 1:
	a = sys.stdin.read(1024)
	if len(a) == 0:
		break
	s.write(a)
	s.flush()
s.close()
