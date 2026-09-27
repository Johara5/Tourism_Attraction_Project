import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Load data
df = pd.read_csv('Tourism_Project/final_data.csv')

# Create Label Encoders
le_continent = LabelEncoder()
le_region = LabelEncoder()
le_attraction = LabelEncoder()
le_visitmode = LabelEncoder()

# Fit encoders
le_continent.fit(df["Continent"])
le_region.fit(df["Region"])
le_attraction.fit(df["AttractionType"])
le_visitmode.fit(df["VisitMode"])

# Transform data for model
X = pd.DataFrame({
    'Continent': le_continent.transform(df["Continent"]),
    'Region': le_region.transform(df["Region"]),
    'AttractionType': le_attraction.transform(df["AttractionType"]),
    'Rating': df["Rating"]
})

y = le_visitmode.transform(df["VisitMode"])

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model and encoders
pickle.dump(model, open("Tourism_Project/visit_mode_model.pkl", "wb"))
pickle.dump(le_continent, open("Tourism_Project/le_continent.pkl", "wb"))
pickle.dump(le_region, open("Tourism_Project/le_region.pkl", "wb"))
pickle.dump(le_attraction, open("Tourism_Project/le_attraction.pkl", "wb"))
pickle.dump(le_visitmode, open("Tourism_Project/le_visitmode.pkl", "wb"))

print("All models and encoders saved successfully!")
print(f"Unique continents: {le_continent.classes_}")
print(f"Unique regions: {le_region.classes_}")
print(f"Unique attraction types: {le_attraction.classes_}")
print(f"Unique visit modes: {le_visitmode.classes_}")
