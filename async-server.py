import asyncore
import socket

HOST='localhost'    # The remote host
PORT=5005           # The same port as used by the client
EOF=';\n'           # Pd FUDI compatibility

class MainServerSocket(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((host,port))
        self.listen(5)
        print "Listening on port", port

    def handle_accept(self):
        newSocket, address = self.accept(  )
        print "Connected from", address
        SecondaryServerSocket(newSocket)


class SecondaryServerSocket(asyncore.dispatcher_with_send):

    def handle_read(self):
        receivedData = self.recv(8192)
        if receivedData:
            print receivedData.rstrip(EOF)
            self.send(receivedData)
        else:
            self.close()

    def handle_close(self):
        print "Disconnected from", self.getpeername()

MainServerSocket(HOST, PORT)
asyncore.loop(  )