import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from architecture import STTN_Model

print("=" * 60)
print("GENERATING ALL IMAGES FOR CUSTOM STTN MODEL")
print("=" * 60)

# ============================================================
# 1. LOAD DATA AND PREPARE
# ============================================================
data_path = r"C:\Users\nazmu\Documents\demo_project\dhaka-green-space-thesis\01_data\master\dhaka_green_space_master.csv"
df = pd.read_csv(data_path)
df = df.dropna(subset=['NDVI', 'NDBI', 'LST', 'LST_Night', 'Population'])

# Create Spatial Lags
df = df.sort_values(['Year', 'grid_id'])
df['LST_neighbor'] = df.groupby('Year')['LST'].shift(1)
df['NDBI_neighbor'] = df.groupby('Year')['NDBI'].shift(1)
df = df.dropna()

feature_cols = ['NDVI', 'NDBI', 'LST_Night', 'Population', 'Year', 'LST_neighbor', 'NDBI_neighbor']
X = df[feature_cols].values.astype(np.float32)
y = df['LST'].values.astype(np.float32)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)

train_loader = DataLoader(TensorDataset(X_train_tensor, y_train_tensor), batch_size=32, shuffle=True)

# Initialize and Train Model (to get the Loss curve)
model = STTN_Model(input_shape=7)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.005)

epochs = 100
train_losses = []

print("Training model to generate graphs (Please wait)...")
for epoch in range(epochs):
    model.train()
    epoch_loss = 0
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()
    train_losses.append(epoch_loss / len(train_loader))

# Predictions for evaluation
model.eval()
with torch.no_grad():
    y_pred = model(X_test_tensor).numpy().flatten()

# Create output folder
output_dir = r"C:\Users\nazmu\Documents\demo_project\dhaka-green-space-thesis\03_results\visualizations"
os.makedirs(output_dir, exist_ok=True)


# ============================================================
# IMAGE 1: SPATIAL HEAT MAP (Dhaka Map)
# ============================================================
print("Generating Image 1: Spatial Heat Map...")
df_2025 = df[df['Year'] == 2025].copy()
X_2025 = scaler.transform(df_2025[feature_cols].values.astype(np.float32))
X_2025_tensor = torch.tensor(X_2025, dtype=torch.float32)

with torch.no_grad():
    pred_2025 = model(X_2025_tensor).numpy().flatten()

df_2025['Predicted_LST'] = pred_2025

plt.figure(figsize=(14, 10))
scatter = plt.scatter(df_2025['lon'], df_2025['lat'], 
                      c=df_2025['Predicted_LST'], 
                      cmap='hot_r', s=15, alpha=0.8, edgecolor='none')
cbar = plt.colorbar(scatter)
cbar.set_label('Predicted LST (°C) - 2025', fontsize=14)
plt.title('Spatial Heat Map of Dhaka (2025) using Custom STTN Model', fontsize=18, fontweight='bold')
plt.xlabel('Longitude', fontsize=14)
plt.ylabel('Latitude', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "STTN_1_Heatmap_2025.png"), dpi=300)
plt.close()


# ============================================================
# IMAGE 2: LOSS CURVE
# ============================================================
print("Generating Image 2: Loss Curve...")
plt.figure(figsize=(10, 6))
plt.plot(range(1, epochs+1), train_losses, color='blue', linewidth=2)
plt.title('STTN Neural Network Training Loss Curve', fontsize=16)
plt.xlabel('Epochs', fontsize=12)
plt.ylabel('Mean Squared Error (Loss)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "STTN_2_Loss_Curve.png"), dpi=300)
plt.close()


# ============================================================
# IMAGE 3: ACTUAL VS PREDICTED
# ============================================================
print("Generating Image 3: Actual vs Predicted...")
plt.figure(figsize=(10, 8))
plt.scatter(y_test, y_pred, alpha=0.3, color='teal', edgecolor='k', s=20)
min_val = min(y_test.min(), y_pred.min())
max_val = max(y_test.max(), y_pred.max())
plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')

r2_final = r2_score(y_test, y_pred)
plt.title(f'Actual vs Predicted LST (R² = {r2_final:.4f})', fontsize=16)
plt.xlabel('Actual LST (°C)', fontsize=12)
plt.ylabel('Predicted LST (°C)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "STTN_3_Actual_vs_Predicted.png"), dpi=300)
plt.close()


# ============================================================
# IMAGE 4: MODEL COMPARISON BAR CHART
# ============================================================
print("Generating Image 4: Model Comparison...")
models = ['Gradient Boosting\n(Baseline)', 'STTN V1\n(No Lags)', 'STTN V2\n(Final)']
spatial_r2 = [0.5919, 0.4576, 0.6638] # From your previous evaluations
colors = ['gray', 'lightcoral', 'forestgreen']

plt.figure(figsize=(10, 6))
bars = plt.bar(models, spatial_r2, color=colors, width=0.5)
plt.title('Spatial Generalization: Baseline vs Custom STTN', fontsize=16)
plt.ylabel('Spatial R² Score', fontsize=12)
plt.ylim(0, 0.8)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.02, round(yval, 4), ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "STTN_4_Model_Comparison.png"), dpi=300)
plt.close()

print("\n" + "=" * 60)
print("✅ ALL 4 IMAGES GENERATED SUCCESSFULLY!")
print(f"📁 Saved in folder: {output_dir}")
print("=" * 60)