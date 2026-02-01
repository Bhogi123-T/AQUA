import pandas as pd
import random

rows = []
FISHS = ["Rohu", "Tilapia", "Catfish", "Seabass", "Carp", "Salmon", "Trout", "Pangasius", "Grouper", "Snapper", "Milkfish", "Barramundi", "Tuna", "Cod"]
PRAWNS = ["Vannamei", "Tiger Prawn", "Freshwater Prawn", "Banana Prawn", "King Prawn", "Whiteleg Shrimp", "Black Tiger Shrimp"]
CRABS = ["Mud Crab", "Blue Swimmer Crab", "King Crab", "Snow Crab", "Dungeness Crab", "Soft Shell Crab"]
ALL_SPECIES = FISHS + PRAWNS + CRABS

for _ in range(10000):
    rows.append([
        random.choice(["USA","China","Japan","EU","India"]),
        random.choice(ALL_SPECIES),
        random.randint(1,50),
        random.choice(["A","B","C"]),
        round(random.uniform(10000, 500000), 2)
    ])

df = pd.DataFrame(rows, columns=["Target_Country","Species","Required_Quantity","Quality_Grade","Price_Offered"])
df.to_csv("dataset/buyer.csv", index=False)
print("✅ Ecosystem Buyer dataset generated")
