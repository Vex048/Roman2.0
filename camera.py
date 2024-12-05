import cv2
import scipy
import tensorflow as tf
from PIL import Image
import numpy as np
model_ = tf.keras.models.load_model("weights/mobilenetV3Large1.h5")

#model2 = tf.keras.models.create_model()

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
while True:
    success, img = cap.read()
    #print("Img_shape",img.shape)
    frame = cv2.resize(img, (224,224))
    #print(frame.shape)

    prediction=model_.predict(frame.reshape(1,224,224,3))
    #print(prediction)
    sm_preferred = tf.nn.softmax(prediction).numpy()
    #print(sm_preferred)
    #print("largest value:",np.max(sm_preferred))
    #print("Smallest value:",np.min(sm_preferred))
    if np.max(sm_preferred)>0.9995:

        cv2.putText(img,str(np.argmax(prediction)), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,
                    cv2.LINE_4)

    #print("category:",np.argmax(prediction))
    cv2.imshow("Gesture Recognition", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()