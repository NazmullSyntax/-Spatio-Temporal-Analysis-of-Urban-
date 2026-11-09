import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from architecture import STTN_Model

print("Generating Visualizations...")

# 1. Load Data
data_path = r"C:\Users\nazmu\Documents\demo_project\dhaka-green-space-thesis\01_data\master\dhaka_green_space_master.csv"
df = pd.read_csv(data_path)
df = df.dropna(subset=['NDVI', 'NDBI', 'LST', 'LST_Night', 'Population'])

# 2. Spatial Lags
df = df.sort_values(['Year', 'grid_id'])
df['LST_neighbor'] = df.groupby('Year')['LST'].shift(1)
df['NDBI_neighbor'] = df.groupby('Year')['NDBI'].shift(1)
df = df.dropna()

feature_cols = ['NDVI', 'NDBI', 'LST_Night', 'Population', 'Year', 'LST_neighbor', 'NDBI_neighbor']
X = df[feature_cols].values.astype(np.float32)
y = df['LST'].values.astype(np.float32)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_train_t = torch.tensor(X_train, dtype=torch.float32)
y_train_t = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
X_test_t = torch.tensor(X_test, dtype=torch.float32)

loader = DataLoader(TensorDataset(X_train_t, y_train_t), batch_size=32, shuffle=True)

# 3. Train Model & Record Loss
model = STTN_Model(input_shape=7)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.005)

train_losses = []
epochs = 100

for epoch in range(epochs):
    model.train()
    epoch_loss = 0
    for bx, by in loader:
        optimizer.zero_grad()
        out = model(bx)
        loss = criterion(out, by)
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()
    train_losses.append(epoch_loss / len(loader))

# 4. Predict
model.eval()
with torch.no_grad():
    y_pred = model(X_test_t).numpy().flatten()

# Create output directory
os.makedirs("../03_results/visualizations", exist_ok=True)

# 5. PLOT 1: Loss Curve
plt.figure(figsize=(10, 6))
plt.plot(range(1, epochs+1), train_losses, color='blue', linewidth=2)
plt.title('STTN Training Loss Curve', fontsize=16)
plt.xlabel('Epochs', fontsize=12)
plt.ylabel('Mean Squared Error (Loss)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("../03_results/visualizations/sttn_loss_curve.png", dpi=300)
plt.close()
print("✅ Saved: sttn_loss_curve.png")

# 6. PLOT 2: Actual vs Predicted
plt.figure(figsize=(10, 10))
plt.scatter(y_test, y_pred, alpha=0.3, color='teal', edgecolor='k', s=20)
# Perfect prediction line
min_val = min(y_test.min(), y_pred.min())
max_val = max(y_test.max(), y_pred.max())
plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')

plt.title(f'Actual vs Predicted LST (R² = {r2_score(y_test, y_pred):.4f})', fontsize=16)
plt.xlabel('Actual LST (°C)', fontsize=12)
plt.ylabel('Predicted LST (°C)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("../03_results/visualizations/sttn_actual_vs_predicted.png", dpi=300)
plt.close()
print("✅ Saved: sttn_actual_vs_predicted.png")

# 7. PLOT 3: Model Comparison Bar Chart
models = ['Gradient Boosting\n(Baseline)', 'STTN V1\n(No Lags)', 'STTN V2\n(Final)']
spatial_r2 = [0.5919, 0.4576, 0.6638]
colors = ['gray', 'lightcoral', 'forestgreen']

plt.figure(figsize=(10, 6))
bars = plt.bar(models, spatial_r2, color=colors, width=0.5)
plt.title('Spatial Generalization: Baseline vs Proposed Architecture', fontsize=16)
plt.ylabel('Spatial R² Score', fontsize=12)
plt.ylim(0, 0.8)

# Add text labels on top of bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.02, round(yval, 4), ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("../03_results/visualizations/model_comparison_bar.png", dpi=300)
plt.close()
print("✅ Saved: model_comparison_bar.png")

print("\nAll visualizations generated successfully!")