# ml/disease_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Define relative paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "datasets", "disease.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "disease.pkl")

# Load dataset
if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

df = pd.read_csv(DATASET_PATH)

# Features to match generate_disease.py and app.py requirements
X = df[["Water_Temp", "pH", "DO", "Salinity", "Turbidity"]]
y = df["Disease_Risk"]

# Train model
model = RandomForestClassifier(n_estimators=20, random_state=42)
model.fit(X, y)

# Save model
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(model, MODEL_PATH)

print(f"Disease model trained and saved successfully to {MODEL_PATH}")
