#!/usr/bin/env python

# Reading an analogue sensor with
# a single GPIO pin

# Author : Matt Hawkins
# Distribution : Raspbian
# Python : 2.7
# GPIO   : RPi.GPIO v3.1.0a

import RPi.GPIO as GPIO
import time
import socket
import errno

# CONST
HOST='pratt.lan'    # The remote host
PORT=5006           # The same port as used by the server
EOF=';\n'           # Pd FUDI compatibility
MAXTRIES=100

# VAR
tries=0
loops=1

# Prepare the socket
# DGRAM=UDP, STREAM=TCP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(5.0)

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

# Main program loop
def main():
    global HOST, PORT, EOF, MAXTRIES
    global s, tries, loops
    try:
        s.connect((HOST, PORT))
        while True:
            # Measure timing using GPIO4
            risetime = RCtime(4)
            # Send to the connected socket
            # (as we're using UDP, we must
            # send separate messages)
            s.sendall('foo %s%s' % (loops, EOF))
            s.sendall('bar %s%s' % (risetime, EOF))
            # Advance counter
            loops = loops + 1
    except socket.error as err:
        errcode = err[0]
        if errcode==errno.ECONNREFUSED:
            print 'Connection refused by host!'
        elif errcode==errno.ENETDOWN:
            print 'No network connection!'
        elif errcode==errno.ENETUNREACH:
            print 'Network unreachable!'
        elif errcode==errno.ENETRESET:
            print 'Network dropped connection!'
        elif errcode==errno.ECONNRESET:
            print 'Connection reset by peer!'
        elif errcode==errno.EHOSTDOWN:
            print 'Host is down!'
        elif errcode==errno.EHOSTUNREACH:
            print 'No route to host!'
        else:
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
        s.close()
        print '%i loops' % loops

main()