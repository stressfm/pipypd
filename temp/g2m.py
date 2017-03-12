import OSC

c = OSC.OSCClient()
c.connect(('localhost', 5008))   # connect to SuperCollider
oscmsg = OSC.OSCMessage()

oscmsg.setAddress("/foo")
oscmsg.append(1000)
c.send(oscmsg)

oscmsg.clear()
oscmsg.setAddress("/bar")
oscmsg.append(0.999)
c.send(oscmsg)
