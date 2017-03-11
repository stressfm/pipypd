#!/usr/bin/env python

import socket
import time
import sys

HOST='pratt.lan'    # The remote host
PORT=5006           # The same port as used by the server
EOF=';\n'           # Pd FUDI compatibility

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
n = 1

try:
  buff = ''
  while True:
    #buff = sys.stdin.readline()
    buff += sys.stdin.read(1)
    if buff.endswith('\n'):
      s.sendall('foo %d%sbar %s%s' % (n, EOF, buff, EOF))
      buff = ''
      n = n + 1
      time.sleep(0.01)
except KeyboardInterrupt:
  sys.stdout.flush()
  s.close()
  pass

print ''
print n
