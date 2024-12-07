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

