    # import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from enum import Enum
from ReachCan import ReachCan.move
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
            
            ColorAcquisition.getColorPosition()
                            
            '''
            # 2 - Get la position de la canette sur l ecran
            '''
            
            ManageCan.move()
            
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