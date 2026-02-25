# ml/yield_model.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv("dataset/yield.csv")

le_species = LabelEncoder()
df['Species_enc'] = le_species.fit_transform(df['Species'])

X = df[['Species_enc', 'Pond_Area', 'Feed_Used', 'Culture_Days']]
y = df['Expected_Yield']

model = RandomForestRegressor(n_estimators=20, random_state=42)
model.fit(X, y)

joblib.dump(model, "models/yield.pkl")
joblib.dump(le_species, "models/le_species_yield.pkl")

print("Yield model trained and saved successfully!")
