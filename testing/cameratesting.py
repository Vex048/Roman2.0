import cv2
import tensorflow as tf
import numpy as np
import time
handValue = None

def checkforHandValue(handValue):
    if handValue == 0:
       handValue = None
       print(0)
       return handValue

    elif handValue == 2:
       handValue = None
       print(2)
       return handValue


    elif handValue == 3:
       handValue = None
       print(3)
       return handValue

    elif handValue == 1:
       handValue = None
       print(1)
       return handValue

interpreter = tf.lite.Interpreter(model_path="weights/converted_model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print(input_details)
print(output_details)

print("Loading camera...")
cam = cv2.VideoCapture(0)
beforeFrame = None
i=0
while True:
    ret, img = cam.read()
    frame = cv2.resize(img, (224,224))    
    input_data = frame.reshape(1,224,224,3)
    input_data = input_data.astype("float32")
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    sm_preferred = tf.nn.softmax(output_data).numpy()
    if np.max(sm_preferred)>=0.9925 and beforeFrame == str(np.argmax(output_data)):
       i+=1
    else:
       i=0
       handValue=None
    beforeFrame = str(np.argmax(output_data)) 
    if i>10:
       handValue = int(np.argmax(output_data))
       handValue = checkforHandValue(handValue)

    k = cv2.waitKey(1)
    if k != -1:
        break
cam.release()
cv2.destroyAllWindows()

