# SmartBin
Dispose Right- Earn Rewards

## 🌍 Project Overview
**SmartBin** is a prototype web application that uses Artificial Intelligence (AI) to classify waste into categories and reward users for disposing of waste correctly.  
This project encourages eco-friendly habits by making waste segregation simple, interactive, and rewarding.  

---

## ✨ Features
- 📷 **Waste Classification**  
  Upload an image of waste (e.g., banana peel, plastic bottle, battery) and the AI model classifies it as:
  - Biodegradable 🍃  
  - Recyclable ♻️  
  - Hazardous ☠️  

- 🗑️ **Disposal Tips**  
  Provides bin-specific disposal instructions (Green = biodegradable, Blue = recyclable, Red = hazardous).  

- ✅ **Proof Verification**  
  Upload a proof image of the disposal bin. The system checks if the bin color matches the expected one.  

- 🏆 **EcoPoints Reward System**  
  - Correct proof = +10 EcoPoints 🌱  
  - Track your total points (stored locally in `rewards.json`).  

---

## 🛠️ Tech Stack
- **Backend:** Flask (Python)  
- **Machine Learning:** TensorFlow/Keras (MobileNetV2 model)  
- **Image Processing:** OpenCV (for bin color verification)  
- **Frontend:** HTML, CSS, JavaScript  
- **Storage:** JSON file (for prototype points tracking)  

---

## 📂 Project Structure
