
import os
import shutil
import random

# Path to your current dataset (all images per class are together now)
SOURCE_DIR = r"d:\216308S\SMART BIN\processed_data"  # change this
DEST_DIR = r"d:\216308S\SMART BIN\dataset"  # where train/validation will be created

# Train/Validation split ratio
TRAIN_RATIO = 0.8  # 80% train, 20% validation

# Get the category folders
categories = [cat for cat in os.listdir(SOURCE_DIR) if os.path.isdir(os.path.join(SOURCE_DIR, cat))]

for category in categories:
    category_path = os.path.join(SOURCE_DIR, category)
    images = os.listdir(category_path)
    random.shuffle(images)

    # Calculate split index
    split_index = int(len(images) * TRAIN_RATIO)
    train_images = images[:split_index]
    val_images = images[split_index:]

    # Paths for train and validation directories
    train_dir = os.path.join(DEST_DIR, "train", category)
    val_dir = os.path.join(DEST_DIR, "validation", category)
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    # Move training images
    for img in train_images:
        shutil.copy(os.path.join(category_path, img), os.path.join(train_dir, img))

    # Move validation images
    for img in val_images:
        shutil.copy(os.path.join(category_path, img), os.path.join(val_dir, img))

print("Dataset split completed successfully!")
