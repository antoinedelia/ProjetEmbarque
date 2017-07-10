class GrabCan(Comportement):

    def move():
        print"attraper la canette"
        writeNumber(Actions.STOP.value)
        time.sleep(1)
        writeNumber(Actions.ENABLEMAGNET.value)
        isGrabbed = True
        time.sleep(2)
        print "Retour zone"
        writeNumber(Actions.BACKWARD.value)
        time.sleep(1)
        writeNumber(Actions.STOP.value)
        time.sleep(1)
