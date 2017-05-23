# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import multiprocessing

import RPi.GPIO as GPIO
import time
import threading
	

GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)

actionGauche = 7
actionDroite = 5
actionAvancer = 3
actionAttraperRelacher = 11
actionCamGauche = 15
actionCamDroite = 13

oldPin = 200
threadFinished = True


def actionRoues(pin):
	if pin == 200 and oldPin != 200:
		#Eteind la led	
		GPIO.setup(oldPin,GPIO.OUT)
		print "LED off"
		GPIO.output(oldPin,GPIO.LOW)
	
	
	if oldPin == pin and oldPin != 200:
		#Allume la led	
		GPIO.setup(pin,GPIO.OUT)
		print "startActionRoues"
		GPIO.output(pin,GPIO.HIGH)
	elif oldPin != 200:
		#Eteind la led
		GPIO.setup(oldPin,GPIO.OUT)
		print "endActionRoues"
		GPIO.output(oldPin,GPIO.LOW)
	
	global oldPin 
	oldPin= pin
	return


def actionAttraperRelacherCanette(str):
	GPIO.setup(actionAttraperRelacher,GPIO.OUT)
	if str == "attraper":
		print "Attraper"
		GPIO.output(actionAttraperRelacher,GPIO.HIGH)
	elif str == "relacher":
		print "Relacher"
		GPIO.output(actionAttraperRelacher,GPIO.LOW)



def actionRotationCamera(actionCam, temps = 0):
	print temps
	wait = int(temps)
	
	if wait != 0:
		threadFinished = False
	
	
	if actionCam == actionCamGauche:
		#GPIO.setup(actionCamGauche,GPIO.OUT)
		
		#GPIO.output(actionCamGauche,GPIO.HIGH)
		
		time.sleep(wait)
		print "Cam Gauche"
		#GPIO.output(actionCamGauche,GPIO.LOW)
		
	elif actionCam == actionCamDroite:
		#GPIO.setup(actionCamDroite,GPIO.OUT)
		
		#GPIO.output(actionCamDroite,GPIO.HIGH)
		
		time.sleep(wait)
		print "Cam Droite"
		#GPIO.output(actionCamDroite,GPIO.LOW)
		
	if wait != 0:
		threadFinished = True


#Load a cascade file for detecting faces
face_cascade = cv2.CascadeClassifier('/home/pi/opencv_regular/opencv-3.2.0/data/haarcascades/haarcascade_frontalface_alt.xml')


# initialize the camera and grab a reference to the raw camera capture
resolutionX = 320
resolutionY = 240

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

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
	gauche = cv2.line(image, ((resolutionX /2)-40, resolutionY), ((resolutionX/2)-40, 0), (255,0,0), 2)
	droite = cv2.line(image, ((resolutionX /2)+40, resolutionY), ((resolutionX/2)+40, 0), (255,255,0), 2)
	hauteur = cv2.line(image, (0, (resolutionY /2)), ((resolutionX, resolutionY/2)), (0,255,0), 2)

	#face=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	#faces = face_cascade.detectMultiScale(face, 1.3, 5)

        '''
	# 1 - Reconnaitre une cannette avec la couleur
	'''
        blur = cv2.blur(image, (3,3))
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_yellow=np.array([20,100,100],dtype=np.uint8)
        upper_yellow=np.array([30,255,255],dtype=np.uint8)

        threshw=cv2.inRange(hsv, lower_yellow, upper_yellow)

        # find contours in the threshold image
        image, contours,hierarchy = cv2.findContours(threshw,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        # finding contour with maximum area and store it as best_cnt
        max_area = 0
        best_cnt = 1
        for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > max_area:
                        max_area = area
                        best_cnt = cnt

        # finding centroids of best_cnt and draw a circle there
        M = cv2.moments(best_cnt)
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        #if best_cnt>1:
        cv2.circle(blur,(cx,cy),10,(0,0,255),-1)

        centreCercle = [cx,cy]
        	
	#Draw a rectangle around every found face
    	cv2.rectangle(image,(cx,cy),(cx+20,cy+20),(255,255,0),2)
	'''
	# 2 - Get la position de la canette sur l ecran
	'''
	#Centre de l'ecran
	centerX = resolutionX / 2
	centerY = resolutionY / 2
		
	if(centreCercle[0] < centerX-40):
		#Canette a gauche
		cv2.putText(image, "Gauche", (150, 230), font, 0.5, (255,255,255),2,cv2.LINE_AA)
		actionRoues(actionGauche)
		actionRotationCamera(actionCamGauche)

	elif(centreCercle[0] > centerX+40):
		#Canette a droite
		cv2.putText(image, "Droite", (150, 230), font, 0.5, (255,255,255),2,cv2.LINE_AA)
		actionRoues(actionDroite)			
		actionRotationCamera(actionCamDroite)

	elif(centreCercle[0] > centerX-40 and centreCercle[0] < centerX+40):
		#Canette au centre
		cv2.putText(image, "Avancer", (150, 230), font, 0.5, (255,255,255),2,cv2.LINE_AA)
		actionRoues(actionAvancer)
		
	'''/////////////////////////
	///////////END FCT//////////
	/////////////////////////'''


	'''
	# 2 - Check si la canette est suffisament proche pour etre attrape ((w*h)carre> 26000pixels)
	'''	

		

	'''
	# 3 - Check si la canette est suffisament proche pour etre attrape ((w*h)carre> 26000pixels)
	'''	
	#if w*h > 26000:
	#	actionAttraperRelacherCanette("attraper")
	#else:
	#	actionAttraperRelacherCanette("relacher")

	'''/////////////////////////
	///////////END FCT//////////
	/////////////////////////'''




	#if not len(faces):
		#Aucune canette
	#	cv2.putText(image, "Rien", (150, 230), font, 0.5, (255,255,255),2,cv2.LINE_AA)
	#	actionRoues(200)
	
	
	
	

	

	# -- Montre l'image
	cv2.imshow("can", image)
	cv2.imshow("frame", blur)
	key = cv2.waitKey(1) & 0xFF
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		breakcamera.resolution = (600, 400)
		cv2.destroyAllWindows()
	




