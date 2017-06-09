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

'''global variable'''
resolutionX = 320
resolutionY = 240


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

#Acquisition
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