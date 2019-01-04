import glob
from shutil import copyfile
import cv2
import logging
logging.basicConfig(filename='logging.log',level=logging.INFO)

def extractset():
    f = glob.glob('/Users/lordvile/Documents/CODE/TESTING RN/Eye tracking/Columbia Gaze Data Set/*')
    for a in f:
        nw = glob.glob(a+'/*.jpg')
        for b in range(3,5):
            image = cv2.imread(nw[b],1)
            res = cv2.resize(image, (600,600))
            cv2.imshow('im',res)
            key = cv2.waitKey(0) & 0xff
            if key==ord('l'):
                copyfile(nw[b],'/Users/lordvile/Documents/CODE/TESTING RN/Eye tracking/dataset/left/{}'.format(nw[b].split('/')[-1]))
                cv2.destroyAllWindows()
            elif key == ord('q'):
                cv2.destroyAllWindows()
                break
            elif key ==ord('r'):
                copyfile(nw[b],'/Users/lordvile/Documents/CODE/TESTING RN/Eye tracking/dataset/right/{}'.format(nw[b].split('/')[-1]))
            elif key ==ord('f'):
                copyfile(nw[b],'/Users/lordvile/Documents/CODE/TESTING RN/Eye tracking/dataset/forward/{}'.format(nw[b].split('/')[-1]))
            else:
                pass

def create_data_set():
    l = ['forward','left','right']
    for name in l:
        f = glob.glob('/Users/lordvile/Documents/CODE/TESTING RN/Eye tracking/dataset/{}/*'.format(name))
        p =0
        bex,bey,bew,beh=0,0,0,0
        eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        eye_glass_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        for a in f:
            logging.info('Started for {}'.format(a))
            img = cv2.imread(a,1)
            img = cv2.flip(img, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
                eyes = eye_glass_cascade.detectMultiScale(roi_gray)
                if(len(eyes)!=0):
                    for (ex,ey,ew,eh) in eyes:
                        if(ex!=0):
                            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                            cv2.imwrite("/Users/lordvile/Documents/CODE/TESTING RN/Eye tracking/dataset/{}/{}_{}.jpg".format(name,name[0],p),roi_color[ey:ey+eh, ex:ex+ew])
               
                p+=1
            logging.info('Done for {}-{}'.format(name[0],p))
#extractset()
create_data_set()
