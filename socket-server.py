import socket

HOST='localhost'
PORT=5005
EOF=';\n'

# create socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# reuse sockets
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((HOST, PORT))
serversocket.listen(5) # become a server socket, maximum 5 connections
conn, addr = serversocket.accept()
print 'connected by ', addr

# listen to connections
while 1:
    buf = conn.recv(64)
    if len(buf) > 0:
        print buf.rstrip(EOF) # do whatever
        
conn.close()