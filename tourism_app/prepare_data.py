import pandas as pd

# Load all Excel files
continent_df = pd.read_excel('Continent.xlsx')
region_df = pd.read_excel('Region.xlsx')
country_df = pd.read_excel('Country.xlsx')
city_df = pd.read_excel('City.xlsx')
type_df = pd.read_excel('Type.xlsx')
mode_df = pd.read_excel('Mode.xlsx')
item_df = pd.read_excel('Item.xlsx')
user_df = pd.read_excel('User.xlsx')
trans_df = pd.read_excel('Transaction.xlsx')

# Manual mapping: AttractionCityId -> Correct location
# All attractions are in Indonesia (Asia, Southeast Asia)
attraction_city_mapping = {
    1: {'Country': 'Indonesia', 'Region': 'Southeast Asia', 'Continent': 'Asia'},
    2: {'Country': 'Indonesia', 'Region': 'Southeast Asia', 'Continent': 'Asia'},
    3: {'Country': 'Indonesia', 'Region': 'Southeast Asia', 'Continent': 'Asia'},
}

# Create mapping dataframe from the manual mapping
mapping_data = []
for city_id, info in attraction_city_mapping.items():
    mapping_data.append({
        'AttractionCityId': city_id,
        'Country': info['Country'],
        'Region': info['Region'],
        'Continent': info['Continent']
    })

attraction_mapping_df = pd.DataFrame(mapping_data)
print("Attraction mapping:")
print(attraction_mapping_df)

# Step 1: Merge Transaction with Item to get attraction details
trans_item = trans_df.merge(
    item_df[['AttractionId', 'AttractionCityId', 'AttractionTypeId', 'Attraction']], 
    on='AttractionId', how='left'
)

# Step 2: Merge with attraction mapping to get correct location (IGNORING City.xlsx)
trans_loc = trans_item.merge(
    attraction_mapping_df,
    on='AttractionCityId',
    how='left'
)

# Step 3: Merge with Type to get Attraction Type
trans_type = trans_loc.merge(
    type_df[['AttractionTypeId', 'AttractionType']], 
    on='AttractionTypeId', how='left'
)

# Step 4: Merge with Mode to get VisitMode name
trans_mode = trans_type.merge(
    mode_df[['VisitModeId', 'VisitMode']], 
    left_on='VisitMode', right_on='VisitModeId', how='left', suffixes=('', '_mode')
)

# Select and rename columns for final dataset
final_df = trans_mode[['UserId', 'Continent', 'Region', 'Attraction', 'AttractionType', 'Rating', 'VisitMode_mode']]
final_df = final_df.rename(columns={'VisitMode_mode': 'VisitMode'})

# Remove rows with missing values
final_df = final_df[final_df['Continent'].notna()]
final_df = final_df[final_df['Region'].notna()]
final_df = final_df[final_df['VisitMode'].notna()]
final_df = final_df[final_df['AttractionType'].notna()]

# Save to CSV
final_df.to_csv('Tourism_Project/final_data.csv', index=False)

print(f"\nFinal dataset shape: {final_df.shape}")
print(f"Unique Continents: {list(final_df['Continent'].unique())}")
print(f"Unique Regions: {list(final_df['Region'].unique())}")
print(f"Unique Attraction Types: {list(final_df['AttractionType'].unique())}")
print(f"Unique Visit Modes: {list(final_df['VisitMode'].unique())}")
print(f"\nSample data:")
print(final_df.head(10))
