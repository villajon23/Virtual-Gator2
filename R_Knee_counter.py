import cv2
import numpy as np
import time
import Ai_PoseModule as pm
#from cvzone.PoseModule import PoseDetector as pm

#use prerecorded datasets (folder name/file name)
cap = cv2.VideoCapture("PoseVideos/c3_v1_s.mp4")
 
detector = pm.PoseDetector()
count = 0
dir = 0
pTime = 0
while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    # img = cv2.imread("AiTrainer/test.jpg")
    img = detector.findPose(img, True) #if true then whole skeleton is drawn on body
    lmList = detector.findPosition(img, False)
    # print(lmList) will print all points of pose
    if len(lmList) != 0:    #check if pose is being detected
        #angle = detector.findAngle(img, 12, 14, 16)     #right arm
        #angle = detector.findAngle(img, 23, 25, 27)     #left leg

        angle = detector.findAngle(img, 24, 26, 28)      #whole right leg(R_hip, R-Knee, R_ankle)
        


        #use values from looking at angle in video to 
        #determin the average min and max value of the action being performed
        #-----------------------------------Checking Knee values----------------------------------------------
        per = np.interp(angle, (187, 280), (0, 100))    #right knee coordiante ranges min and max when performed in dataset
        bar = np.interp(angle, (187, 280), (650, 100))
    
        # print(angle, per)q
 
        # Check for bent knee and straight knee 
        color = (255, 0, 255)   #standard color
        if per == 100:
            color = (0, 255, 0) #if reaches the value then new color on meter
            if dir == 1: #bending knee
                count += 0.5    #add 0.5 to the count then goes down and u get 1 full count
                dir = 0 #straightening knee out
        if per == 0:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1 
        print(count)
 
        # Draw meter Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4)         
 
        # Draw knee count 
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