    # import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2
import numpy as np
import multiprocessing
import RPi.GPIO as GPIO
import time
import threading
import smbus
import sys
import signal
import Communication
import Sonar


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

#Interrupt Signal

"""Thread"""

tScan = threading.Thread(target=Camera.Camera(), args=([mutexVideo, mutexSonar]))
tSonar = threading.Thread(target=Sonar.Sonar(), args=([mutexSonar]))

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