import cv2
import tensorflow as tf
import numpy as np
import time
import settings


	

def opencv(stop,model_):
	print("Loading camera...")
	cam = cv2.VideoCapture(0)
	cam.set(3,1280)
	cam.set(4,720)
	beforeFrame = None
	i=0
	while True:
		if stop():
			break
		ret, img = cam.read()
		frame = cv2.resize(img, (224,224))
		prediction=model_.predict(frame.reshape(1,224,224,3))
		sm_preferred = tf.nn.softmax(prediction).numpy()
		if np.max(sm_preferred)>0.95 and beforeFrame == str(np.argmax(prediction)) :
			i+=1
		else:
			i=0
			settings.handValue = None
		beforeFrame = str(np.argmax(prediction))
		if i>15:
			settings.handValue = int(np.argmax(prediction))
			returnValueFromHand()
			cv2.putText(img, str(np.argmax(prediction)), (200,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,
                    cv2.LINE_4)
			
		cv2.imshow('Imagetest',img)
		k = cv2.waitKey(1)
		if k != -1:
			break
	cam.release()
	cv2.destroyAllWindows()
	

def returnValueFromHand():
        if settings.handValue == 0:
            print("FIST")
            time.sleep(3)
        elif settings.handValue == 1:
            print("ONE")
            time.sleep(3)
        elif settings.handValue == 2:
            print("PALM")
            time.sleep(3)
        elif settings.handValue == 3:
            print("THREE")
            time.sleep(3)