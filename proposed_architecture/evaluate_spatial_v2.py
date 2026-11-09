import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from architecture import STTN_Model

print("=" * 60)
print("DAY 5: STTN V2 with Spatial Features (Lagging)")
print("=" * 60)

# 1. Load Data
data_path = r"C:\Users\nazmu\Documents\demo_project\dhaka-green-space-thesis\01_data\master\dhaka_green_space_master.csv"
df = pd.read_csv(data_path)
df = df.dropna(subset=['NDVI', 'NDBI', 'LST', 'LST_Night', 'Population'])

# 2. CREATE SPATIAL LAG FEATURES
# Sort by year and grid_id to properly shift data
df = df.sort_values(['Year', 'grid_id'])

# Create a feature representing the previous grid cell's LST (Proxy for spatial context)
df['LST_neighbor'] = df.groupby('Year')['LST'].shift(1)
df['NDBI_neighbor'] = df.groupby('Year')['NDBI'].shift(1)
df = df.dropna() # Drop the first row of each year since it has no neighbor

# 3. Define Features
feature_cols = ['NDVI', 'NDBI', 'LST_Night', 'Population', 'Year', 'LST_neighbor', 'NDBI_neighbor']
X = df[feature_cols].values.astype(np.float32)
y = df['LST'].values.astype(np.float32)

# 4. Spatial Bins
df['lat_bin'] = pd.cut(df['lat'], bins=5, labels=False)
groups = df['lat_bin'].values

gkf = GroupKFold(n_splits=5)
spatial_r2_scores = []

for fold, (train_idx, test_idx) in enumerate(gkf.split(X, y, groups=groups)):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
    X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)
    
    train_loader = DataLoader(TensorDataset(X_train_tensor, y_train_tensor), batch_size=32, shuffle=True)
    
    # Note: Input shape is now 7 features instead of 5
    model = STTN_Model(input_shape=7) 
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.005)
    
    model.train()
    for epoch in range(50):
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            
    model.eval()
    with torch.no_grad():
        y_pred = model(X_test_tensor).numpy().flatten()
        
    r2 = r2_score(y_test, y_pred)
    spatial_r2_scores.append(r2)
    print(f"Fold {fold + 1} R²: {r2:.4f}")

print("\n" + "=" * 60)
print("SPATIAL VALIDATION RESULTS (STTN V2)")
print("=" * 60)
print(f"Mean Spatial R²: {np.mean(spatial_r2_scores):.4f}")
print(f"Std Dev:         {np.std(spatial_r2_scores):.4f}")
print("=" * 60)