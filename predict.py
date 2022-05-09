import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import keras

#new_model = tf.keras.models.load_model('Final_model_95p007.h5')
#new_model = tf.keras.models.load_model("C:\Users\Brandy Odhiambo\Documents\project\flask-blog-tutorial-master\new_model.h5")
new_model = keras.models.load_model('new_model.h5')

def predict_mood(): 
    print('Just about to start Execution, kindly be patient')
    #cv2.namedWindow('Users name Here')
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) #takes a zero since its your computer camera, if it were an external camera feeding frames to 
                            #your computer, replace zero with 1

    i = 0
    x = 255
    y = 208
    h = 170
    w = 168

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        #define cascade classifiers
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        
        #get gray scale image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        #detect images
        faces = faceCascade.detectMultiScale(gray,1.1,4)
        
        
        for x,y,w,h in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            facess = faceCascade.detectMultiScale(roi_gray)
            if len(facess) != 0:
                print("Face detected {}".format(str(i)))
                for(ex,ey,ew,eh) in facess:
                        face_roi = roi_color[ey:ey+eh,ex:ex+ew]
                        
                        
        
        i = i+1 
        
        final_image = cv2.resize(frame,(224,224))
        final_image = np.expand_dims(final_image,axis=0)
        final_image = final_image/255.0
        predictions = new_model.predict(final_image)
        prediction = np.argmax(predictions)
        status = ''
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        if(prediction==0):
            status = "Angry"
            x1,y1,w1,h1=0,0,175,75
            cv2.putText(frame,status,(100,150),font,3, (0,0,255),2,cv2.LINE_4)
            cv2.rectangle(frame,(x,y),(x+w, y+h),(0,0,255))

        elif(prediction==1):
            status = "Disgust"
            x1,y1,w1,h1=0,0,175,75
            cv2.putText(frame,status,(100,150),font,3,(0,0,255),2,cv2.LINE_4)
            cv2.rectangle(frame,(x,y),(x+w, y+h),(0,0,255))

        elif(prediction==2):
            status = "Fear"
            x1,y1,w1,h1=0,0,175,75
            cv2.putText(frame,status,(100,150),font,3,(0,0,255),2,cv2.LINE_4)
            cv2.rectangle(frame,(x,y),(x+w, y+h),(0,0,255))

        elif(prediction==3):
            status = "Happy"
            x1,y1,w1,h1=0,0,175,75
            cv2.putText(frame,status,(100,150),font,3,(0,0,255),2,cv2.LINE_4)
            cv2.rectangle(frame,(x,y),(x+w, y+h),(0,0,255))

        elif(prediction==4):
            status = "Sad"
            x1,y1,w1,h1=0,0,175,75
            cv2.putText(frame,status,(100,150),font,3,(0,0,255),2,cv2.LINE_4)
            cv2.rectangle(frame,(x,y),(x+w, y+h),(0,0,255))

        elif(prediction==5):
            status = "Surprise"
            x1,y1,w1,h1=0,0,175,75
            
            cv2.putText(frame,status,(100,150),font,3,(0,0,255),2,cv2.LINE_4)
            cv2.rectangle(frame,(x,y),(x+w, y+h),(0,0,255))

        else: 
            status = "Neutral"
            x1,y1,w1,h1=0,0,175,75
            cv2.putText(frame,status,(100,150),font,3,(0,0,255),2,cv2.LINE_4)
            cv2.rectangle(frame,(x,y),(x+w, y+h),(0,0,255))
            
        cv2.imshow('User name shoud infact be here', frame)    
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break
    #Save
    
    #send to the doctor    

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    return (frame, status)




predict_mood()    

