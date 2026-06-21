import pandas as pd
import random
from faker import Faker

fake = Faker()
rows = []

FISHS = ["Rohu", "Tilapia", "Catfish", "Seabass", "Carp", "Salmon", "Trout", "Pangasius", "Grouper", "Snapper", "Milkfish", "Barramundi", "Tuna", "Cod"]
PRAWNS = ["Vannamei", "Tiger Prawn", "Freshwater Prawn", "Banana Prawn", "King Prawn", "Whiteleg Shrimp", "Black Tiger Shrimp"]
CRABS = ["Mud Crab", "Blue Swimmer Crab", "King Crab", "Snow Crab", "Dungeness Crab", "Soft Shell Crab"]
ALL_SPECIES = FISHS + PRAWNS + CRABS

countries = ["India", "Vietnam", "Thailand", "Indonesia", "Bangladesh"]
states = ["Andhra Pradesh", "West Bengal", "Odisha", "Tamil Nadu", "Gujarat", "Kerala", "Bihar", "Mekong Delta", "Can Tho", "Bac Lieu", "Soc Trang", "Ca Mau", "Chonburi", "Rayong", "Trat", "Surat Thani", "Nakorn Si Thammarat", "Java", "Sumatra", "Bali", "Sulawesi", "Kalimantan", "Chittagong", "Khulna", "Barisal", "Sylhet", "Rajshahi"]

for _ in range(10000):
    spec = random.choice(ALL_SPECIES)
    atype = "Fish" if spec in FISHS else ("Prawn" if spec in PRAWNS else "Crab")
    rows.append([
        random.choice(countries),
        random.choice(states),
        fake.city(),
        round(random.uniform(-10,30), 4),
        round(random.uniform(60,100), 4),
        random.choice(["Tropical", "Subtropical"]),
        random.choice(["Summer", "Monsoon", "Winter"]),
        atype,
        spec,
        random.randint(40, 100)
    ])

df = pd.DataFrame(rows, columns=["Country", "State", "District", "Latitude", "Longitude", "Climate_Zone", "Season", "Aqua_Type", "Species", "Suitability_Score"])
df.to_csv("dataset/location.csv", index=False)
print("✅ Ecosystem Location dataset generated")
