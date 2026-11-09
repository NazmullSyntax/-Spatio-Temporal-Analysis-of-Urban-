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

# Define a flexible model for ablation
class STTN_Ablation(nn.Module):
    def __init__(self, input_shape, use_dropout=True, use_batchnorm=True):
        super(STTN_Ablation, self).__init__()
        
        layers1 = [nn.Linear(input_shape, 64)]
        if use_batchnorm: layers1.append(nn.BatchNorm1d(64))
        layers1.append(nn.ReLU())
        if use_dropout: layers1.append(nn.Dropout(0.1))
        self.layer1 = nn.Sequential(*layers1)
        
        layers2 = [nn.Linear(64, 32), nn.ReLU()]
        if use_dropout: layers2.append(nn.Dropout(0.1))
        self.layer2 = nn.Sequential(*layers2)
        
        self.layer3 = nn.Sequential(nn.Linear(32, 16), nn.ReLU())
        self.output_layer = nn.Linear(16, 1)
        
    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.output_layer(x)
        return x

print("=" * 60)
print("DAY 6: Ablation Study (Testing Component Importance)")
print("=" * 60)

# Load Data
data_path = r"C:\Users\nazmu\Documents\demo_project\dhaka-green-space-thesis\01_data\master\dhaka_green_space_master.csv"
df = pd.read_csv(data_path)
df = df.dropna(subset=['NDVI', 'NDBI', 'LST', 'LST_Night', 'Population'])

# Add Spatial Lags
df = df.sort_values(['Year', 'grid_id'])
df['LST_neighbor'] = df.groupby('Year')['LST'].shift(1)
df['NDBI_neighbor'] = df.groupby('Year')['NDBI'].shift(1)
df = df.dropna()

feature_cols = ['NDVI', 'NDBI', 'LST_Night', 'Population', 'Year', 'LST_neighbor', 'NDBI_neighbor']
X = df[feature_cols].values.astype(np.float32)
y = df['LST'].values.astype(np.float32)

df['lat_bin'] = pd.cut(df['lat'], bins=5, labels=False)
groups = df['lat_bin'].values

gkf = GroupKFold(n_splits=5)

def run_experiment(use_dropout, use_batchnorm, label):
    print(f"\n--- Running: {label} ---")
    scores = []
    
    for fold, (train_idx, test_idx) in enumerate(gkf.split(X, y, groups=groups)):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        
        X_tr_tensor = torch.tensor(X_train, dtype=torch.float32)
        y_tr_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
        X_te_tensor = torch.tensor(X_test, dtype=torch.float32)
        
        loader = DataLoader(TensorDataset(X_tr_tensor, y_tr_tensor), batch_size=32, shuffle=True)
        
        model = STTN_Ablation(input_shape=7, use_dropout=use_dropout, use_batchnorm=use_batchnorm)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.005)
        
        model.train()
        for epoch in range(30): # Using 30 epochs for speed
            for bx, by in loader:
                optimizer.zero_grad()
                out = model(bx)
                loss = criterion(out, by)
                loss.backward()
                optimizer.step()
                
        model.eval()
        with torch.no_grad():
            pred = model(X_te_tensor).numpy().flatten()
            scores.append(r2_score(y_test, pred))
            
    print(f"{label} Mean Spatial R²: {np.mean(scores):.4f}")
    return np.mean(scores)

# 1. Full Model
full_score = run_experiment(use_dropout=True, use_batchnorm=True, label="Full Model (Dropout + BatchNorm)")

# 2. Without Dropout
no_dropout_score = run_experiment(use_dropout=False, use_batchnorm=True, label="Ablation 1: Without Dropout")

# 3. Without BatchNorm
no_bn_score = run_experiment(use_dropout=True, use_batchnorm=False, label="Ablation 2: Without Batch Normalization")

print("\n" + "=" * 60)
print("ABLATION SUMMARY")
print("=" * 60)
print(f"Full Model:        {full_score:.4f}")
print(f"Without Dropout:   {no_dropout_score:.4f}")
print(f"Without BatchNorm: {no_bn_score:.4f}")