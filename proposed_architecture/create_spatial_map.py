import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from architecture import STTN_Model

print("Generating Spatial Prediction Map using Custom STTN...")

# 1. Load Data
data_path = r"C:\Users\nazmu\Documents\demo_project\dhaka-green-space-thesis\01_data\master\dhaka_green_space_master.csv"
df = pd.read_csv(data_path)
df = df.dropna(subset=['NDVI', 'NDBI', 'LST', 'LST_Night', 'Population'])

# 2. Create Spatial Lags (Crucial for our new model)
df = df.sort_values(['Year', 'grid_id'])
df['LST_neighbor'] = df.groupby('Year')['LST'].shift(1)
df['NDBI_neighbor'] = df.groupby('Year')['NDBI'].shift(1)
df = df.dropna()

# 3. Filter data for 2025 (to map the current situation)
df_2025 = df[df['Year'] == 2025].copy()
print(f"Total grid cells for 2025: {len(df_2025)}")

# 4. Setup Features & Scaler
feature_cols = ['NDVI', 'NDBI', 'LST_Night', 'Population', 'Year', 'LST_neighbor', 'NDBI_neighbor']

# We must fit the scaler on the ENTIRE dataset to ensure consistency with training
X_all = df[feature_cols].values.astype(np.float32)
scaler = StandardScaler()
scaler.fit(X_all) 

# Scale the 2025 data
X_2025 = scaler.transform(df_2025[feature_cols].values.astype(np.float32))
X_2025_tensor = torch.tensor(X_2025, dtype=torch.float32)

# 5. Load the Trained Model
model = STTN_Model(input_shape=7)
model_path = r"../03_results/models/final_sttn_model.pth" # Adjust path if needed
model.load_state_dict(torch.load(model_path))
model.eval()

# 6. Predict LST for 2025
with torch.no_grad():
    predictions = model(X_2025_tensor).numpy().flatten()

df_2025['STTN_Predicted_LST'] = predictions

# 7. Create the Map
plt.figure(figsize=(14, 10))

# Scatter plot using Longitude and Latitude
scatter = plt.scatter(df_2025['lon'], df_2025['lat'], 
                      c=df_2025['STTN_Predicted_LST'], 
                      cmap='hot_r', # 'hot_r' is good for temperature (yellow=cool, red=hot)
                      s=15, 
                      alpha=0.8,
                      edgecolor='none')

# Add Colorbar
cbar = plt.colorbar(scatter)
cbar.set_label('Predicted Land Surface Temperature (°C) - 2025', fontsize=14)

# Add Titles and Labels
plt.title('Spatial Heat Map of Dhaka (2025) using Custom STTN Model', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Longitude', fontsize=14)
plt.ylabel('Latitude', fontsize=14)

# Add a grid for better readability
plt.grid(True, linestyle='--', alpha=0.5)

# Save the figure
output_path = "../03_results/visualizations/sttn_heatmap_2025.png"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.tight_layout()
plt.savefig(output_path, dpi=300)
plt.close()

print(f"✅ Spatial Map generated successfully: {output_path}")