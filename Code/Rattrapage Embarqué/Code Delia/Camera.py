import Can

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
        Setup()

        if areas :
            cnt2 = contours[np.argmax(areas)]
            tx,ty,tw,th = cv2.boundingRect(cnt2)
            cv2.rectangle(blur,(tx,ty),(tx+tw,ty+th),(0,255,255),2)

            if tw*th > 26000:
                if(isGrabbed == False):
                    Can.GrabCan()
                else:
                    Can.ReleaseCan()
                
        # finding centroids of best_cnt and draw a circle there
        M = cv2.moments(best_cnt)
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        #if best_cnt>1:
        cv2.circle(blur,(cx,cy),10,(0,0,255),-1)
        centreCercle = [cx,cy]
        
        Can.aller_chercher()

def Setup(self):
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