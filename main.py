<<<<<<< HEAD
import server
import settings
import threading
import voice
import tensorflow as tf
from camera import opencv
model_ = tf.keras.models.load_model("weights/mobilenetV3Large1.h5")



settings.init()
t2 = threading.Thread(target=server.run)
t3 = threading.Thread(target=voice.startSR,args=(model_,))
t2.start()
t3.start()

=======
import server
import settings
import threading
import voice
import tensorflow as tf
from camera import opencv
#model_ = tf.keras.models.load_model("weights/mobilenetV3Large1.h5")
interpreter=tf.lite.Interpreter(model_path="weights/converted_model.tflite")
interpreter.allocate_tensors()


settings.init()
t2 = threading.Thread(target=server.run)
t3 = threading.Thread(target=voice.startSR,args=(interpreter,))
t2.start()
t3.start()

>>>>>>> 7ae0a8575beda5c985a01ab99816cf4c0ae8f63a
