import pandas as pd
import random

rows = []

for _ in range(10000):
    disease = random.choice([0,1])
    rows.append([
        round(random.uniform(24,32),1),
        round(random.uniform(6.5,8.5),2),
        round(random.uniform(4,7),2),
        round(random.uniform(5,25),2),
        round(random.uniform(10,60),2),
        disease,
        "White Spot" if disease else "None",
        "Lime Treatment" if disease else "None"
    ])

df = pd.DataFrame(rows, columns=[
    "Water_Temp","pH","DO","Salinity","Turbidity",
    "Disease_Risk","Disease_Type","Suggested_Medicine"
])

df.to_csv("dataset/disease.csv", index=False)
print("✅ Disease dataset generated")
