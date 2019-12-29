import struct; import sys; page = open(sys.argv[1]).read(); data = struct.unpack("<BhhhB", page); offset = 2 ; print "%.02f" % (float(data[3] - offset) / (4096 * 0.0625));



