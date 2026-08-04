import tensorflow as tf

MODEL_PATH = "model/best_model.keras"

SAVE_PATH = "model/tf_lite/skin_model.tflite"

model = tf.keras.models.load_model(MODEL_PATH)

converter = tf.lite.TFLiteConverter.from_keras_model(model)

converter.optimizations = [

    tf.lite.Optimize.DEFAULT

]

tflite_model = converter.convert()

with open(

    SAVE_PATH,

    "wb"

) as f:

    f.write(tflite_model)

print("Đã export TensorFlow Lite.")

print(SAVE_PATH)