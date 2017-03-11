import asyncore
import socket

HOST='localhost'    # The remote host
PORT=5005           # The same port as used by the client
EOF=';\n'           # Pd FUDI compatibility

class CallHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            print data.rstrip(EOF)
            # self.send(data)

class CallServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = CallHandler(sock)

    def handle_close(self):
        print 'handle_close'

    def handle_connect(self):
        print 'handle_connect'

server = CallServer(HOST, PORT)
print 'listening on %s:%s' % (HOST, PORT)
asyncore.loop()