class ColorAcquisition(Acquisition):
    def getColorPosition():
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
                
        # finding centroids of best_cnt and draw a circle there
        M = cv2.moments(best_cnt)
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        #if best_cnt>1:
        cv2.circle(blur,(cx,cy),10,(0,0,255),-1)
        centreCercle = [cx,cy]