#!/usr/bin/env python

# Reading an analogue sensor with
# a single GPIO pin

# Author : Matt Hawkins
# Distribution : Raspbian
# Python : 2.7
# GPIO   : RPi.GPIO v3.1.0a

import RPi.GPIO as GPIO
import time
import errno
import OSC

# CONST
HOST='pratt.lan'    # The remote host
PORT=5008           # The same port as used by the server
MAXTRIES=100

# VAR
tries = 0
loops = 1

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
oscmsg = OSC.OSCMessage()
c.connect((HOST, PORT))   # connect to SuperCollider

# Main program loop
def main ():
    global MAXTRIES
    global tries, loops
    try:
      while True:
        # Measure timing using GPIO4
        risetime = RCtime(4)
        # Send to the connected socket
        oscmsg.clear()
        oscmsg.setAddress("/foo")
        oscmsg.append(loops)
        c.send(oscmsg)

        oscmsg.clear()
        oscmsg.setAddress("/bar")
        oscmsg.append(float(risetime))
        c.send(oscmsg)

        # Advance counter
        loops = loops + 1
    except OSC.OSCClientError as err:
        print 'Caught: %s!' % err

        if tries >= MAXTRIES:
            GPIO.cleanup()
            s.close()
            print 'No connection. Exiting.'
        else:
            print 'Tried %i of %i times.\nWaiting %is...' % (tries, MAXTRIES, tries/10)
            time.sleep(tries/10)
            tries = tries + 1
            main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print '%i loops' % loops

main()