#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
#host = socket.gethostname() # Get local machine name
port = 59000                # Reserve a port for your service.

s.connect(("Bernardo", port))

s.send("Puta �s tu?")
print (s.recv(1024))
s.close                     # Close the socket when done