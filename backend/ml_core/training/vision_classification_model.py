import os
import json
import tensorflow as tf
from tensorflow.keras import layers, models # type: ignore
from tensorflow.keras.applications import MobileNetV2 # type: ignore
from tensorflow.keras.preprocessing.image import ImageDataGenerator # type: ignore

# ==============================================================================
# AQUA Platform - Advanced Image Classification System for Aquatic Species
# ==============================================================================
# This script builds and trains a Convolutional Neural Network (CNN) 
# to accurately classify new, unseen images of fishes, prawns, and other life.
# It uses Transfer Learning (MobileNetV2) which provides high recognition accuracy.
# ==============================================================================

# Configuration
DATASET_DIR = os.path.join(os.path.dirname(__file__), '../datasets/aquatic_images')
MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), '../models/aqua_vision_model.keras')
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10

def build_model(num_classes):
    """
    Builds a custom classification model on top of MobileNetV2
    """
    # Load the base model with pre-trained weights (excluding the top classification layer)
    base_model = MobileNetV2(
        input_shape=IMG_SIZE + (3,),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze the base model to retain learned features and ensure fast training
    base_model.trainable = False
    
    # Create the custom classification head for aquatic species
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.3), # Prevent overfitting on small datasets
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes, activation='softmax') # Output layer for species classification
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_system():
    print("Initializing AQUA Vision Classification Training...")
    
    if not os.path.exists(DATASET_DIR):
        print(f"Error: Dataset directory {DATASET_DIR} not found.")
        print("Creating directory structure. Please add images to subfolders.")
        os.makedirs(os.path.join(DATASET_DIR, 'fishes'), exist_ok=True)
        os.makedirs(os.path.join(DATASET_DIR, 'prawns'), exist_ok=True)
        os.makedirs(os.path.join(DATASET_DIR, 'crabs'), exist_ok=True)
        return

    # Data augmentation for better generalization on unseen images
    # This prevents the model from memorizing images and improves real-world accuracy
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=0.2 # 20% of data for validation
    )

    # Load training data
    train_generator = train_datagen.flow_from_directory(
        DATASET_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='sparse',
        subset='training'
    )

    # Load validation data
    val_generator = train_datagen.flow_from_directory(
        DATASET_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='sparse',
        subset='validation'
    )
    
    num_classes = len(train_generator.class_indices)
    print(f"Detected {num_classes} species classes: {train_generator.class_indices}")
    
    if num_classes == 0:
        print("No images found. Please add images to the dataset directory.")
        return

    model = build_model(num_classes)
    model.summary()

    print("Starting training to improve recognition accuracy...")
    
    # Add early stopping to get the best model
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_accuracy', 
        patience=3, 
        restore_best_weights=True
    )
    
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=val_generator,
        callbacks=[early_stopping]
    )
    
    # Save the highly accurate model
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    model.save(MODEL_SAVE_PATH)
    print(f"Model successfully saved to {MODEL_SAVE_PATH}")
    
    # Save class indices mapping for predictions
    class_indices_path = os.path.join(os.path.dirname(MODEL_SAVE_PATH), 'vision_classes.json')
    with open(class_indices_path, 'w') as f:
        # Swap keys and values for easier prediction lookup
        index_to_class = {v: k for k, v in train_generator.class_indices.items()}
        json.dump(index_to_class, f)
        
    print("Training complete! The system is now ready to classify unseen fishes and prawns.")

if __name__ == "__main__":
    train_system()
