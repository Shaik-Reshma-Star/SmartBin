import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Load model
model = tf.keras.models.load_model("model/smartbin.keras")

# Class names (order must match your training)
class_names = ["biodegradable", "hazardous","recyclable"]

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    predicted_class = class_names[np.argmax(predictions)]
    confidence = round(100 * np.max(predictions), 2)

    return predicted_class, confidence

# Example usage
label, conf = predict_image("test_images/b1.jpg")
print(f"Prediction: {label} ({conf}% confidence)")
