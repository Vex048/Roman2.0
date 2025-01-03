import tensorflow as tf
from tensorflow.contrib import lite
converter = lite.TFLiteConverter.from_keras_model_file('weights/mobilenetV3Large1.h5')
tfmodel = converter.convert()
open ("model1.tflite" , "wb") .write(tfmodel)
