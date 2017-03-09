import socket
import time
import math

HOST='localhost'    # The remote host
PORT=5006           # The same port as used by the server
EOF=';\n'           # Pd FUDI compatibility
msg='foo 2002%s' % EOF

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
n=1
while n<1001:
    # m=math.sqrt(n*3)
    m='BQ'
    s.sendall('foo %s%sbar %s%s' % (n, EOF, m, EOF))
    n=n+1
    time.sleep(0.1)

s.close()
