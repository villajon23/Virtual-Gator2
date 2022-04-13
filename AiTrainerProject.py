import cv2
import numpy as np
import time
import Ai_PoseModule as pm
#from cvzone.PoseModule import PoseDetector as pm
 
cap = cv2.VideoCapture("PoseVideos/c3_v1_s.mp4")
 
detector = pm.PoseDetector()
count = 0
dir = 0
pTime = 0
while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    # img = cv2.imread("AiTrainer/test.jpg")
    img = detector.findPose(img, False) #if true then whole skeleton is drawn on body
    lmList = detector.findPosition(img, False)
    # print(lmList) will print all points of pose
    if len(lmList) != 0:    #check if pose is being detected
        #angle = detector.findAngle(img, 12, 14, 16)     #right arm
        #angle = detector.findAngle(img, 28, 26, 24)    #right leg
        #angle = detector.findAngle(img, 23, 25, 27)     #left leg
        angle = detector.findAngle(img, 11, 25, 23 )    # leftknee to shoulder

        #angle = detector.findAngle(img, 23, 25, 27,False)  #left leg
        

        #use values from looking at angle in video to 
        #determin the average min and max value of the action being performed
        per = np.interp(angle, (290, 270), (0, 100))    #high and low angle range, convert to 0 to 100
        bar = np.interp(angle, (290, 270), (650, 100))  #(min,max) value of bar
        # print(angle, per)
 
        # Check for the dumbbell curls
        color = (255, 0, 255)   #standard color
        if per == 100:
            color = (0, 255, 0) #if reaches the value then new color on meter
            if dir == 0: #going up
                count += 0.5    #add 0.5 to the count then goes down and u get 1 full count
                dir = 1 #going down
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0 
        print(count)
 
        # Draw Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4)
 
        # Draw Curl Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)   #draws the box with count
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)
 
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)
 
    cv2.imshow("Image", img)
    if cv2.waitKey(10) & 0xFF==ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()