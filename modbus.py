import socket
import sys
import serial
import serial.rs485

ser = serial.rs485.RS485("/dev/ttyAMA0", 19200, timeout=1)
ser.rs485_mode = serial.rs485.RS485Settings(False, True)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_address = ("localhost", 2020)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
sock.listen(1)

while True:
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'client connected:', client_address
        while True:
            data = connection.recv(256)
            print >>sys.stderr, 'received "%s"' % data
            if data:
                ser.write(data)
            else:
                break
            serdata = ser.read(256)
            if serdata:
                connection.sendall(serdata)
    finally:
        connection.close()
