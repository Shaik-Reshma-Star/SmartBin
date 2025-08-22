from flask import Flask, render_template, request, redirect, url_for
import tensorflow as tf
import numpy as np
import cv2
import os
import json
from tensorflow.keras.preprocessing import image


app = Flask(__name__)



# Load ML Model
MODEL_PATH = "model/smartbin.keras"
model = tf.keras.models.load_model(MODEL_PATH)

# Labels
class_labels = ['biodegradable', 'hazardous', 'recyclable']

# Disposal Tips
disposal_tips = {
    "biodegradable": "Dispose in compost (green bin).",
    "hazardous": "Dispose in red bin at hazardous waste point.",
    "recyclable": "Dispose in blue bin for recycling."
}

# Expected bin colors (BGR format ranges for OpenCV)
bin_colors = {
    "biodegradable": {"lower": (35, 100, 100), "upper": (85, 255, 255)},   # Green
    "hazardous": {"lower": (0, 100, 100), "upper": (10, 255, 255)},        # Red
    "recyclable": {"lower": (100, 100, 100), "upper": (140, 255, 255)}     # Blue
}

# Rewards storage
REWARD_FILE = "rewards.json"
if not os.path.exists(REWARD_FILE):
    with open(REWARD_FILE, "w") as f:
        json.dump({"points": 0}, f)

def get_points():
    with open(REWARD_FILE, "r") as f:
        return json.load(f)["points"]

def add_points(pts):
    # Read first
    current_points = get_points()
    new_points = current_points + pts
    
    # Then overwrite safely
    with open(REWARD_FILE, "w") as f:
        json.dump({"points": new_points}, f)

# ---- Routes ----
@app.route("/")
def index():
    return render_template("index.html", points=get_points())

@app.route("/classify", methods=["POST"])
def classify():
    file = request.files["waste_image"]
    if not file:
        return redirect(url_for("index"))

    filepath = os.path.join("static", "uploaded.jpg")
    file.save(filepath)

    # Preprocess image
    img = image.load_img(filepath, target_size=(224, 224))
    img_array = np.expand_dims(image.img_to_array(img), axis=0) / 255.0

    predictions = model.predict(img_array)
    predicted_class = class_labels[np.argmax(predictions)]
    confidence = float(np.max(predictions) * 100)

    return render_template("proof.html",
                           waste_type=predicted_class,
                           confidence=round(confidence, 2),
                           tip=disposal_tips[predicted_class],
                           points=get_points())

@app.route("/verify", methods=["POST"])
def verify():
    waste_type = request.form["waste_type"]
    proof_file = request.files["proof_image"]

    if not proof_file:
        return redirect(url_for("index"))

    proof_path = os.path.join("static", "proof.jpg")
    proof_file.save(proof_path)

    # Check bin color
    img = cv2.imread(proof_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,
                       bin_colors[waste_type]["lower"],
                       bin_colors[waste_type]["upper"])
    match_percentage = (cv2.countNonZero(mask) / (img.shape[0] * img.shape[1])) * 100

    if match_percentage > 5:  # Threshold
        add_points(10)
        return render_template("success.html", points=get_points(), success=True)
    else:
        return render_template("success.html", points=get_points(), success=False)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5500))  # Default to 5500 if PORT is not set
    app.run(port=port, debug=True)

