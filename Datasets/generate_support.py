import pandas as pd
import random

rows = []

for _ in range(50000):
    rows.append([
        random.choice(["Disease","Water","Feed"]),
        random.randint(1,72),
        round(random.uniform(70,98),2),
        round(random.uniform(3.5,5),2)
    ])

df = pd.DataFrame(rows, columns=[
    "Issue_Type","Resolution_Time_Hrs",
    "Success_Rate","Technician_Rating"
])

df.to_csv("dataset/technician_support_50k.csv", index=False)
print("✅ Support dataset generated")
