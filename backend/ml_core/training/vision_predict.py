import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image # type: ignore

# ==============================================================================
# AQUA Platform - Inference Script for Image Classification
# ==============================================================================
# This script loads the trained model and uses it to automatically classify 
# unseen images of fishes, prawns, and other aquatic life with high accuracy.
# ==============================================================================

MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), '../models/aqua_vision_model.keras')
CLASS_INDICES_PATH = os.path.join(os.path.dirname(__file__), '../models/vision_classes.json')
IMG_SIZE = (224, 224)

def load_system():
    if not os.path.exists(MODEL_SAVE_PATH):
        raise FileNotFoundError("Model not found. Please run vision_classification_model.py first.")
    
    if not os.path.exists(CLASS_INDICES_PATH):
        raise FileNotFoundError("Class mapping not found. Please train the model first.")

    model = tf.keras.models.load_model(MODEL_SAVE_PATH)
    
    with open(CLASS_INDICES_PATH, 'r') as f:
        class_mapping = json.load(f)
        
    return model, class_mapping

def classify_unseen_image(image_path, model, class_mapping):
    """
    Classifies a new, unseen image using the trained deep learning model.
    """
    if not os.path.exists(image_path):
        return {"error": f"Image file not found at {image_path}"}
        
    print(f"Analyzing image: {image_path}...")
    
    # Preprocess the image to match the training data
    img = image.load_img(image_path, target_size=IMG_SIZE)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) # Create a batch
    img_array = img_array / 255.0 # Rescale as done in training
    
    # Run the prediction
    predictions = model.predict(img_array)
    predicted_class_index = str(np.argmax(predictions[0]))
    confidence = float(np.max(predictions[0]))
    
    predicted_species = class_mapping.get(predicted_class_index, "Unknown")
    
    result = {
        "species": predicted_species,
        "confidence": round(confidence * 100, 2),
        "status": "High Accuracy" if confidence > 0.8 else "Low Confidence - Consider Retraining"
    }
    
    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Classify an unseen aquatic image.')
    parser.add_argument('--image', type=str, required=True, help='Path to the image file (e.g., test_fish.jpg)')
    
    args = parser.parse_args()
    
    try:
        model, class_mapping = load_system()
        result = classify_unseen_image(args.image, model, class_mapping)
        
        print("\n--- CLASSIFICATION RESULT ---")
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Detected Organism: {result['species'].upper()}")
            print(f"Recognition Confidence: {result['confidence']}%")
            print(f"Status: {result['status']}")
            print("-----------------------------\n")
            
    except Exception as e:
        print(f"System Error: {e}")
