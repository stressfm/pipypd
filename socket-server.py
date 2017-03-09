import socket

HOST='localhost'    # The remote host
PORT=5005           # The same port as used by the client
EOF=';\n'           # Pd FUDI compatibility

# create socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# reuse sockets
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((HOST, PORT))
serversocket.listen(5) # become a server socket, maximum 5 connections
conn, addr = serversocket.accept()
print 'connected by ', addr

try:
    while 1:
        buf = conn.recv(512)
        if len(buf) > 0:
            print buf.rstrip(EOF) # do whatever
except Exception as e:
    print e
# listen to connections
        
conn.close()