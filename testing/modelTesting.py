import cv2
import tensorflow as tf
import numpy as np
import time
import settings


model1 = tf.keras.models.load_model("weights/mobilenetV3Large1.h5")
model2 = tf.keras.models.load_model("weights/EfficentNetB2_reloaded.h5")
cam = cv2.VideoCapture(0)
cam.set(3,1280)
cam.set(4,720)
beforeFrame = None
i=0
while True:
    ret, img = cam.read()
    frame = cv2.resize(img, (224,224))
    prediction=model2.predict(frame.reshape(1,224,224,3))
    sm_preferred = tf.nn.softmax(prediction).numpy()
    print(sm_preferred)
    if np.max(sm_preferred)>0.99 and beforeFrame == str(np.argmax(prediction)) :
        i+=1
    else:
        i=0
    beforeFrame = str(np.argmax(prediction))
    if i>15:
        cv2.putText(img, str(np.argmax(prediction)), (200,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,
                cv2.LINE_4)
        
    cv2.imshow('Imagetest',img)
    k = cv2.waitKey(1)
    if k != -1:
        break
cam.release()
cv2.destroyAllWindows()
	