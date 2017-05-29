    # import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from enum import Enum
import cv2
import numpy as np
import multiprocessing
import RPi.GPIO as GPIO
import time
import threading
import smbus
import sys
import signal

class Actions(Enum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4
    STOP = 5
    ENABLEMAGNET = 6
    DISABLEMAGNET = 7

'''global variable'''
resolutionX = 320
resolutionY = 240
bus = smbus.SMBus(1)
address = 0x04
isGrabbed=False
threadFinished = True
target = False
centreCercle = [0,0]
distance = 100
''' END Global Variable  '''

camera = PiCamera()
camera.resolution = (resolutionX, resolutionY)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=camera.resolution )
     
# allow the camera to warmup
time.sleep(0.1)
#init la position du carre a 0
cx = 0
cy = 0      
positions = ''
font = cv2.FONT_HERSHEY_SIMPLEX
center = []

#define threads
mutexSonar = threading.Event()
mutexVideo = threading.Event()

def writeNumber(value):
    bus.write_byte(address, value)
    return -1

def readNumber():
    number = bus.read_byte(address)
    return number

def Sonar(mutexSonar):
    while True:
      # Use BCM GPIO references
      # instead of physical pin numbers
      GPIO.setmode(GPIO.BCM)
      # Define GPIO to use on Pi
      GPIO_TRIGGER = 21
      GPIO_ECHO    = 26
      # Set pins as output and input
      GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  
      GPIO.setup(GPIO_ECHO,GPIO.IN)  
      # Set trigger to False (Low)
      GPIO.output(GPIO_TRIGGER, False)
      # Allow module to settle
      time.sleep(0.5)
      # Send 10us pulse to trigger
      GPIO.output(GPIO_TRIGGER, True)
      time.sleep(0.00001)
      GPIO.output(GPIO_TRIGGER, False)
      start = time.time()
      while GPIO.input(GPIO_ECHO)==0:
        start = time.time()
      while GPIO.input(GPIO_ECHO)==1:
        stop = time.time()
      # Calculate pulse length
      elapsed = stop-start
      # Distance pulse travelled in that time is time
      # multiplied by the speed of sound (cm/s)
      global distance
      distance = elapsed * 34300
      # That was the distance there and back so halve the value
      distance = distance / 2
      #print "Distance : %.1f" % distance
      # Reset GPIO settings
      GPIO.cleanup()
      
    return distance


def Camera(mutexVideo, mutexSonar):
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            global isGrabbed
            global distance
            global target
            global centreCercle
            '''=
            # 1 - Reconnaitre une cannette avec la couleur
            '''
            blur = cv2.blur(image, (3,3))
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            lower_red=np.array([150,150,50],dtype=np.uint8)
            upper_red=np.array([180,255,255],dtype=np.uint8)

            lower_yellow=np.array([20,100,100],dtype=np.uint8)
            upper_yellow=np.array([30,255,255],dtype=np.uint8)

            if(isGrabbed == False):
                threshw=cv2.inRange(hsv, lower_yellow, upper_yellow)
            else:
                threshw=cv2.inRange(hsv, lower_red, upper_red)

            #threshw=cv2.inRange(hsv, lower_red, upper_red)
            #threshw=cv2.inRange(hsv, lower_yellow, upper_yellow)

            # find contours in the threshold image
            image, contours,hierarchy = cv2.findContours(threshw,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

            # finding contour with maximum area and store it as best_cnt
            max_area = 0
            best_cnt = 1
            areas = [cv2.contourArea(c) for c in contours]
            for cnt in contours:
                    area = cv2.contourArea(cnt)
                    if area > max_area:
                            max_area = area
                            best_cnt = cnt
            if areas :
                    cnt2 = contours[np.argmax(areas)]
                    tx,ty,tw,th = cv2.boundingRect(cnt2)
                    cv2.rectangle(blur,(tx,ty),(tx+tw,ty+th),(0,255,255),2)

                    if tw*th > 26000:
                        if(isGrabbed == False):
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
                        else:
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
                    
            # finding centroids of best_cnt and draw a circle there
            M = cv2.moments(best_cnt)
            cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
            #if best_cnt>1:
            cv2.circle(blur,(cx,cy),10,(0,0,255),-1)
            centreCercle = [cx,cy]
                            
            '''
            # 2 - Get la position de la canette sur l ecran
            '''
            
            #print distance
            aller_chercher()
            
            '''
            # 3 - Check si la canette est suffisament proche pour etre attrape ((w*h)carre> 26000pixels)
            '''	
            # -- Montre l'image
            
            cv2.imshow("can", image)
            cv2.imshow("frame", blur)
            key = cv2.waitKey(1) & 0xFF
            rawCapture.truncate(0)
     
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                    global breakcamera
                    breakcamera.resolution = (600, 400)
                    cv2.destroyAllWindows()

def recherche():
    global distance
    global target
    #pattern de recherche
    print distance
    if(target==False):
        if(distance>15):
            writeNumber(Actions.FORWARD.value)

        elif(distance<=15):
            writeNumber(Actions.LEFT.value)
        
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
            recherche()
                    
    elif(centreCercle[0] < centerX-40):
            target=True
            #Canette a gauche
            #cv2.putText(image, "Gauche", (150, 230), font, 0.5, (255,255,255),2,cv2.LINE_AA)
            writeNumber(Actions.LEFT.value)

    elif(centreCercle[0] > centerX+40):
            target=True
            #Canette a droite
            #cv2.putText(image, "Droite", (150, 230), font, 0.5, (255,255,255),2,cv2.LINE_AA)		
            writeNumber(Actions.RIGHT.value)

    elif(centreCercle[0] > centerX-40 and centreCercle[0] < centerX+40 and isGrabbed == False):
            #Canette au centre
            target=True
            #cv2.putText(image, "Avancer", (150, 230), font, 0.5, (255,255,255),2,cv2.LINE_AA)
            writeNumber(Actions.FORWARD.value)


#Interrupt Signal

"""Thread"""

tScan = threading.Thread(target=Camera, args=([mutexVideo, mutexSonar]))
tSonar = threading.Thread(target=Sonar, args=([mutexSonar]))

try:
        tScan.start()
	tSonar.start()
        
except Exception as ex:
    print ex
except KeyboardInterrupt:
    print "Attempting to close threads"
    mutexSonar.clear()
    mutexVideo.clear()
    tScan.join()
    tSonar.join()
    print "Threads successfully closed"


