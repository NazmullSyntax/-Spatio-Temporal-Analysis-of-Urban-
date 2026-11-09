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
print("DAY 8: Final Spatial Cross-Validation (The Real Test)")
print("=" * 60)

# 1. Load Data
data_path = r"C:\Users\nazmu\Documents\demo_project\dhaka-green-space-thesis\01_data\master\dhaka_green_space_master.csv"
df = pd.read_csv(data_path)
df = df.dropna(subset=['NDVI', 'NDBI', 'LST', 'LST_Night', 'Population'])

# 2. Spatial Lags (Crucial)
df = df.sort_values(['Year', 'grid_id'])
df['LST_neighbor'] = df.groupby('Year')['LST'].shift(1)
df['NDBI_neighbor'] = df.groupby('Year')['NDBI'].shift(1)
df = df.dropna()

# 3. Features & Target
feature_cols = ['NDVI', 'NDBI', 'LST_Night', 'Population', 'Year', 'LST_neighbor', 'NDBI_neighbor']
X = df[feature_cols].values.astype(np.float32)
y = df['LST'].values.astype(np.float32)

# 4. Spatial Bins (Groups)
df['lat_bin'] = pd.cut(df['lat'], bins=5, labels=False)
groups = df['lat_bin'].values

gkf = GroupKFold(n_splits=5)
spatial_r2_scores = []

print("Starting Spatial Validation...\n")

for fold, (train_idx, test_idx) in enumerate(gkf.split(X, y, groups=groups)):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    X_train_t = torch.tensor(X_train, dtype=torch.float32)
    y_train_t = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
    X_test_t = torch.tensor(X_test, dtype=torch.float32)
    
    loader = DataLoader(TensorDataset(X_train_t, y_train_t), batch_size=32, shuffle=True)
    
    model = STTN_Model(input_shape=7)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.005)
    
    model.train()
    for epoch in range(50):
        for bx, by in loader:
            optimizer.zero_grad()
            out = model(bx)
            loss = criterion(out, by)
            loss.backward()
            optimizer.step()
            
    model.eval()
    with torch.no_grad():
        pred = model(X_test_t).numpy().flatten()
        r2 = r2_score(y_test, pred)
        spatial_r2_scores.append(r2)
        print(f"Fold {fold + 1} R²: {r2:.4f}")

print("\n" + "=" * 60)
print("FINAL SPATIAL VALIDATION RESULTS (STTN V2)")
print("=" * 60)
print(f"Mean Spatial R²: {np.mean(spatial_r2_scores):.4f}")
print(f"Std Dev:         {np.std(spatial_r2_scores):.4f}")
print("=" * 60)