import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Load the trained model
model = load_model("model/smartbin.keras")

# Class labels (must match training order)
class_labels = ['biodegradable', 'hazardous', 'recyclable']

# Load and preprocess the test image
img_path = "test_images/bd2.jpg"  # change this path
img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = img_array / 255.0  # normalize

# Predict
predictions = model.predict(img_array)
predicted_class = class_labels[np.argmax(predictions)]

print(f"Predicted Class: {predicted_class}")
print(f"Confidence: {np.max(predictions) * 100:.2f}%")
