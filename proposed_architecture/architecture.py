"""
Custom Machine Learning Architecture: Spatio-Temporal Tabular Network (STTN)
Author: [Your Name]
Project: Spatio-Temporal Analysis and Future Prediction of Urban Green Space Loss in Dhaka City

Day 7 Update: Removed BatchNorm based on Ablation Study findings. 
Final configuration: Dropout (0.1), Spatial Lags, No BatchNorm.
"""

import torch
import torch.nn as nn

class STTN_Model(nn.Module):
    """
    Spatio-Temporal Tabular Network (STTN) using PyTorch.
    Optimized for spatial generalization in urban heat prediction.
    """
    def __init__(self, input_shape):
        super(STTN_Model, self).__init__()
        
        # 1. First Hidden Layer (Feature Extraction)
        # Removed BatchNorm to preserve spatial variation
        self.layer1 = nn.Sequential(
            nn.Linear(input_shape, 64),
            nn.ReLU(),
            nn.Dropout(0.1) 
        )
        
        # 2. Second Hidden Layer
        self.layer2 = nn.Sequential(
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.1) 
        )
        
        # 3. Third Hidden Layer
        self.layer3 = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU()
        )
        
        # 4. Output Layer
        self.output_layer = nn.Linear(16, 1)
        
    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.output_layer(x)
        return x