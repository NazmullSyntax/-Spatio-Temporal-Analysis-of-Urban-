"""
Custom Machine Learning Architecture: Spatio-Temporal Tabular Network (STTN)
Author: [Your Name]
Project: Spatio-Temporal Analysis and Future Prediction of Urban Green Space Loss in Dhaka City

Updated on Day 3: Reduced Dropout to 0.1 for better feature retention.
"""

import torch
import torch.nn as nn

class STTN_Model(nn.Module):
    """
    Spatio-Temporal Tabular Network (STTN) using PyTorch.
    Custom architecture for predicting Land Surface Temperature.
    """
    def __init__(self, input_shape):
        super(STTN_Model, self).__init__()
        
        # 1. First Hidden Layer (Feature Extraction)
        self.layer1 = nn.Sequential(
            nn.Linear(input_shape, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.1) # Updated from 0.2 to 0.1
        )
        
        # 2. Second Hidden Layer (Deep Relationship)
        self.layer2 = nn.Sequential(
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.1) # Updated from 0.2 to 0.1
        )
        
        # 3. Third Hidden Layer (Compression)
        self.layer3 = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU()
        )
        
        # 4. Output Layer (Regression Target: LST)
        self.output_layer = nn.Linear(16, 1)
        
    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.output_layer(x)
        return x

if __name__ == "__main__":
    # Test the model
    model = STTN_Model(input_shape=5)
    print(model)
    
    # Print total parameters
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Total Parameters: {total_params}")