import cv2
import tensorflow as tf
import numpy as np
import time
import settings
from server import startPlayback, stopPlayback,nextPlayback,prevPlayback,resumePlayback

	

def opencv(interpreter):
	print("Loading camera...")
	cam = cv2.VideoCapture(0)
	beforeFrame = None
	i=0
	input_details = interpreter.get_input_details()
	output_details = interpreter.get_output_details()
	while True:
		if settings.stop_threads == True:
			settings.stop_threads= False
			break
		ret, img = cam.read()
		frame = cv2.resize(img, (224,224))
		input_data = frame.reshape(1,224,224,3)
		input_data = input_data.astype("float32")
		interpreter.set_tensor(input_details[0]['index'],input_data)
		interpreter.invoke()
		prediction = interpreter.get_tensor(output_details[0]['index'])
		sm_preferred = tf.nn.softmax(prediction).numpy()
		if np.max(sm_preferred)>=0.9925 and beforeFrame == str(np.argmax(prediction)) :
			i+=1
		else:
			i=0
			settings.handValue = None
		beforeFrame = str(np.argmax(prediction))
		if i>10:
			settings.handValue = int(np.argmax(prediction))
			checkforHandValue()
			i=0

	cam.release()
	cv2.destroyAllWindows()
	


def checkforHandValue():
    if settings.handValue == 0:
        settings.handValue = None
        print("Hand sign read: Fist")
        resumePlayback()
    elif settings.handValue == 2:
        settings.handValue = None
        print("Hand sign read: Palm")
        stopPlayback()  
    elif settings.handValue == 3:
        settings.handValue = None
        print("Hand sign read: Three")
        nextPlayback()
    elif settings.handValue == 1:
        settings.handValue = None
        print("Hand sign read: One")
        prevPlayback()
       
