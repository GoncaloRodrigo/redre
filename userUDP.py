import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
message = 'This is the message.  It will be repeated.'

try:

    # Send data
    print ('sending "%s"' % message,file=sys.stderr)
    sent = sock.sendto(message.encode(), server_address)

    # Receive response
    print ( 'waiting to receive',file=sys.stderr)
    data, server = sock.recvfrom(4096)
    print ('received "%s"' % data.decode(), file=sys.stderr)

finally:
    print  ('closing socket',file=sys.stderr)
    sock.close()