import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from architecture import STTN_Model

print("=" * 60)
print("DAY 2: Training Custom STTN Neural Network (PyTorch)")
print("=" * 60)

# 1. Load Data
data_path = r"C:\Users\nazmu\Documents\demo_project\dhaka-green-space-thesis\01_data\master\dhaka_green_space_master.csv"
df = pd.read_csv(data_path)
df = df.dropna(subset=['NDVI', 'NDBI', 'LST', 'LST_Night', 'Population'])
print(f"Loaded Rows: {len(df)}")

# 2. Features and Target
feature_cols = ['NDVI', 'NDBI', 'LST_Night', 'Population', 'Year']
X = df[feature_cols].values.astype(np.float32)
y = df['LST'].values.astype(np.float32)

# 3. Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Convert to PyTorch Tensors
X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

# Create DataLoader for batching
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# 6. Initialize Model, Loss, and Optimizer
model = STTN_Model(input_shape=5)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# 7. Training Loop
print("\nStarting Training...")
epochs = 50
for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()       # Clear previous gradients
        outputs = model(batch_X)    # Forward pass
        loss = criterion(outputs, batch_y) # Calculate loss
        loss.backward()             # Backward pass
        optimizer.step()            # Update weights
        running_loss += loss.item()
        
    if (epoch + 1) % 10 == 0:
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {running_loss/len(train_loader):.4f}")

# 8. Evaluation
print("\nEvaluating Model...")
model.eval()
with torch.no_grad():
    y_pred_tensor = model(X_test_tensor)
    y_pred = y_pred_tensor.numpy().flatten()

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n" + "=" * 60)
print("STTN NEURAL NETWORK RESULTS")
print("=" * 60)
print(f"MAE:  {mae:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"R²:   {r2:.4f}")
print("=" * 60)

# 9. Save Model
os.makedirs("../03_results/models", exist_ok=True)
torch.save(model.state_dict(), "../03_results/models/sttn_custom_model.pth")
print("Model saved to: 03_results/models/sttn_custom_model.pth")