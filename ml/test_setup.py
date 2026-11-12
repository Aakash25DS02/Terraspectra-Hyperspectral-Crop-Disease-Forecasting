import torch
import numpy as np
import sys
import os

print("Python version:", sys.version)
print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
print("NumPy version:", np.__version__)

# Test basic tensor operations
x = torch.randn(3, 64, 64, 100)  # Hyperspectral cube example
print("Test tensor shape:", x.shape)

# Check if we can import our config
try:
    from config import Config
    print("Config loaded successfully!")
    print("Device:", Config.DEVICE)
except Exception as e:
    print("Config error:", e)
