#!/usr/bin/env python

# Reading an analogue sensor with
# a single GPIO pin

# Author : Matt Hawkins
# Distribution : Raspbian
# Python : 2.7
# GPIO   : RPi.GPIO v3.1.0a

import RPi.GPIO as GPIO
import time
import OSC

HOST='pratt.lan'    # The remote host
PORT=5008           # The same port as used by the server
EOF=';\n'           # Pd FUDI compatibility

# Tell the GPIO library to use
# Broadcom GPIO references
GPIO.setmode(GPIO.BCM)

# Measures charge time
def RCtime (PiPin):
  measurement = 0
  # Discharge capacitor
  GPIO.setup(PiPin, GPIO.OUT)
  GPIO.output(PiPin, GPIO.LOW)
  time.sleep(0.1)

  GPIO.setup(PiPin, GPIO.IN)
  # Count loops until voltage across
  # capacitor reads high on GPIO
  start = time.time()
  while (GPIO.input(PiPin) == GPIO.LOW):
    measurement += 1

  end = time.time()
  # print end - start
  # return measurement
  return str(end - start)

# Connects the socket
c = OSC.OSCClient()
oscmsg = ''
def connect ():
    try:
        c.connect((HOST, PORT))   # connect to SuperCollider
        oscmsg = OSC.OSCMessage()
    except Exception as err:
      print err
      pass

# Main program loop
n = 1
connect()
try:
  while True:
    # Measure timing using GPIO4
    risetime = RCtime(4)
    # Send to the connected socket
    # (as we're using UDP, we must
    # send separate messages)
    oscmsg.clear()
    oscmsg.setAddress("/foo")
    oscmsg.append(n)
    c.send(oscmsg)

    oscmsg.clear()
    oscmsg.setAddress("/bar")
    oscmsg.append(risetime)
    c.send(oscmsg)

    # Advance counter
    n = n + 1
except KeyboardInterrupt:
  GPIO.cleanup()
  s.close()
  print ''
  pass

print n