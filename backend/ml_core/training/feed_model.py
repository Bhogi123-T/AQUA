# ml/feed_model.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv("dataset/feed.csv")

le_species = LabelEncoder()
le_feed = LabelEncoder()

df['Species_enc'] = le_species.fit_transform(df['Species'])
df['Feed_Type_enc'] = le_feed.fit_transform(df['Feed_Type'])

X = df[['Species_enc', 'Age_Days', 'Water_Temp', 'DO', 'Feed_Type_enc', 'Protein']]
y = df['Feed_Quantity']

model = RandomForestRegressor(n_estimators=20, random_state=42)
model.fit(X, y)

joblib.dump(model, "models/feed.pkl")
joblib.dump(le_species, "models/le_species_feed.pkl")
joblib.dump(le_feed, "models/le_feed.pkl")

print("Feed model trained and saved successfully!")
