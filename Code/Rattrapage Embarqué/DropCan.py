class DropCan(Comportement):

    def move():
        print"relacher la canette"
        writeNumber(Actions.STOP.value)
        time.sleep(1)
        writeNumber(Actions.DISABLEMAGNET.value)
        isGrabbed = False
        time.sleep(2)
        writeNumber(Actions.BACKWARD.value)
        time.sleep(1)
        writeNumber(Actions.LEFT.value)
        time.sleep(1)
        writeNumber(Actions.STOP.value)
        time.sleep(1)
        print "Recherche canette"
