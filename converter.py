import tensorflow as tf

model = tf.keras.models.load_model("weights/mobilenetV3Large1.h5")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
open("weights/converted_model.tflite", "wb").write(tflite_model)