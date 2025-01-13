import tensorflow as tf
import numpy as np
interpreter = tf.lite.Interpreter(model_path="weights/converted_model.tflite")
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
interpreter.allocate_tensors()
print(input_details)
print(output_details)
