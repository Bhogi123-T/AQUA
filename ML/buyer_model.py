# ml/buyer_model.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv("dataset/buyer.csv")

le_country = LabelEncoder()
le_species = LabelEncoder()
le_grade = LabelEncoder()

df['Country_enc'] = le_country.fit_transform(df['Target_Country'])
df['Species_enc'] = le_species.fit_transform(df['Species'])
df['Grade_enc'] = le_grade.fit_transform(df['Quality_Grade'])

X = df[['Country_enc', 'Species_enc', 'Required_Quantity', 'Grade_enc']]
y = df['Price_Offered']

model = RandomForestRegressor(n_estimators=20, random_state=42)
model.fit(X, y)

joblib.dump(model, "models/buyer.pkl")
joblib.dump(le_country, "models/le_country_buyer.pkl")
joblib.dump(le_species, "models/le_species_buyer.pkl")
joblib.dump(le_grade, "models/le_grade_buyer.pkl")

print("Buyer model trained and saved successfully!")
