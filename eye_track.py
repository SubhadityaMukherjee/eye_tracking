import numpy as np
import cv2
import time


eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
eye_glass_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
left_counter=0  
right_counter=0 
    
th_value=5   

def thresholding( value ):
    global left_counter
    global right_counter
    
    if (value<=54):   
        left_counter=left_counter+1

        if (left_counter>th_value):
            print('RIGHT')  
            left_counter=0  

    elif(value>=54):  
        right_counter=right_counter+1

        if(right_counter>th_value):
            print('LEFT')
            right_counter=0

def main(inp):
    cap = cv2.VideoCapture(0)
    p =0
    bex,bey,bew,beh=0,0,0,0
    while 1:
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = inp.detectMultiScale(roi_gray)
            if(len(eyes)!=0 and p%30==0):
                for (ex,ey,ew,eh) in eyes:
                    if(ex!=0):
                        bex,bey,bew,beh = ex,ey,ew,eh
                        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                        cv2.imwrite("eyes/eye_{}.jpg".format(p),roi_color[ey:ey+eh, ex:ex+ew])
            else:
                print(bex,bey,bew,beh)
                cv2.rectangle(roi_color,(bex,bey),(bex+bew,bey+beh),(0,255,0),2)
                cv2.imwrite("eyes/eyen_{}.jpg".format(p),roi_color[bey:bey+beh, bex:bex+bew])
            p+=1

        cv2.imshow('img',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def choice():
    n = int(input('1 if you wear glasses, 2 if you dont '))
    if n ==1:
        main(eye_glass_cascade)
    else:
        main(eye_cascade)
choice()
1121
