import Communication
import Actions

def aller_chercher():
    global distance
    global target
    global centreCercle
    global resolutionX
    global resolutionY
    
    #Centre de l'ecran
    centerX = resolutionX / 2
    centerY = resolutionY / 2
    
    if centreCercle == [0,0]:
            #print "no target"
            target = False
            SearchCan()
                    
    elif(centreCercle[0] < centerX-40):
            target=True
            #Canette a gauche
            #cv2.putText(image, "Gauche", (150, 230), font, 0.5, (255,255,255),2,cv2.LINE_AA)
            Communication.writeNumber(Actions.Actions.LEFT.value)

    elif(centreCercle[0] > centerX+40):
            target=True
            #Canette a droite
            #cv2.putText(image, "Droite", (150, 230), font, 0.5, (255,255,255),2,cv2.LINE_AA)		
            Communication.writeNumber(Actions.Actions.RIGHT.value)

    elif(centreCercle[0] > centerX-40 and centreCercle[0] < centerX+40 and isGrabbed == False):
            #Canette au centre
            target=True
            #cv2.putText(image, "Avancer", (150, 230), font, 0.5, (255,255,255),2,cv2.LINE_AA)
            Communication.writeNumber(Actions.Actions.FORWARD.value)

def SearchCan():
    global distance
    global target
    #pattern de recherche
    print distance
    if(target == False):
        if(distance>15):
            writeNumber(Actions.FORWARD.value)

        elif(distance<=15):
            writeNumber(Actions.LEFT.value)

def GrabCan():
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

def ReleaseCan():
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