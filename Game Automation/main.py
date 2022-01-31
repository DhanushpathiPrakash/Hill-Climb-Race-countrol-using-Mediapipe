# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 09:54:08 2022

@author: Dhanushpathi Prakash
"""

import cv2
import mediapipe as mp
import time
from directkeys import right_pressed,left_pressed
from directkeys import PressKey, ReleaseKey


break_key_pressed=left_pressed
accelerato_key_pressed=right_pressed

time.sleep(2.0)
current_key_pressed = set()

mp_draw=mp.solutions.drawing_utils #Draw the  hand pose
mp_hand=mp.solutions.hands #solution for hand

tipIds=[4,8,12,16,20] #to identify tip of all fingers
video=cv2.VideoCapture(0)

with mp_hand.Hands(min_detection_confidence=0.5,
                   min_tracking_confidence=0.5)as hands:
    while True:
        keyPressed = False
        break_pressed = False
        accelerato_pressed = False
        key_count=0
        key_Pressed=0
        ret,image=video.read() #return image or video
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #color convert from bgr to rgb in cv
        image.flags.writeable=False
        results=hands.process(image) #again return the processed image
        image.flags.writeable=True #again write process image
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #processed image color convertor
        lmList=[]
        if results.multi_hand_landmarks: #hand land mark https://media.geeksforgeeks.org/wp-content/uploads/20210802154942/HandLandmarks.png
            for hand_landmark in results.multi_hand_landmarks:
                myHands=results.multi_hand_landmarks[0] #strating point of a landmark
                for id, lm in enumerate(myHands.landmark): # coordinate of the axis in landmarl
                    h,w,c=image.shape #height and weight of frame
                    cx,cy= int(lm.x*w), int(lm.y*h) #coordinate axis  value
                    lmList.append([id,cx,cy]) #list for coordinate
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS) #hand coco model
        fingers=[]
        if len(lmList)!=0:
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1,5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total=fingers.count(1)
            #print(total)
            if total==0:
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "BRAKE", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                PressKey(break_key_pressed)
                break_pressed=True
                current_key_pressed.add(break_key_pressed)
                key_pressed=break_key_pressed
                keyPressed = True
                key_count=key_count+1
            elif total==5:
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, " GAS", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                PressKey(accelerato_key_pressed)
                key_pressed=accelerato_key_pressed
                accelerator_pressed=True
                keyPressed = True
                current_key_pressed.add(accelerato_key_pressed)
                key_count=key_count+1
        if not keyPressed and len(current_key_pressed) != 0:
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()
        elif key_count==1 and len(current_key_pressed)==2:    
            for key in current_key_pressed:             
                if key_pressed!=key:
                    ReleaseKey(key)
            current_key_pressed = set()
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()              
    
        #    if lmList[8][2] < lmList[6][2]:
        #       print("open")
        #   else:
        #      print("Close")
        cv2.imshow("Frame", image)
        k=cv2.waitKey(1)
        if k==ord('q'):
            break
video.release()
cv2.destroyAllWindows()