from math import *
import threading
from enum import Enum
''' Global Variable '''
resolutionX = 320
resolutionY = 240
''' END Global Variable  '''

def TaskCamera():
    camera = Camera()
    camera.start()
    pass
def task2():
    print "1"
    pass

def dep1():
    t1 = threading.Thread(target=TaskCamera)
    t2 = threading.Thread(target=task2)
    t1.start()
    t2.start()

class Camera(object):
    image = None
    def __init__(self,*observers):
        self.observes = observers
        self.camera = PiCamera()
        self.camera.resolution = (resolutionX, resolutionY)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(camera, size=camera.resolution )
    def start()
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
    def event(self):
        for obs in self.observes:
            obs.notify(image)
        print "event with",data
    

class ColorAquisition:
    #def __init__(self,color):
        
    def angle(x,y):
        return degrees(atan2(x,y))
            
    def Recherche():

            '''=
                # 1 - Reconnaitre une cannette avec la couleur
            '''
            blur = cv2.blur(image, (3,3))
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            if color == "red":
                lower_color=np.array([150,150,50],dtype=np.uint8)
                upper_color=np.array([180,255,255],dtype=np.uint8)
            elif color == "yellow":
                lower_color=np.array([20,100,100],dtype=np.uint8)
                upper_color=np.array([30,255,255],dtype=np.uint8)
            
            threshw=cv2.inRange(hsv, lower_color, upper_color)
            image, contours,hierarchy = cv2.findContours(threshw,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            
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
                x,y,w,h = cv2.boundingRect(cnt2)
                cv2.rectangle(blur,(x,y),(x+w,y+h),(0,255,255),2)
                angle(x+w/2,y+h/2)
                surface = w*h;
                return angle , surface
            return
        

class Deplacement:
    def __init__(self,):
        self.countDetection = 0
        self.ListPos =[]


class Observer(object):
    def notify(self,*args,**kwargs):
        print args,kwargs

t = Camera(Observer())
t.event()
