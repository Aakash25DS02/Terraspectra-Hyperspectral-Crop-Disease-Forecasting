import torch
import os

class Config:
    # Device configuration
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # Data parameters
    PATCH_SIZE = 64
    BATCH_SIZE = 32
    NUM_WORKERS = 4
    
    # Model parameters
    NUM_CLASSES = 5  # Different crop disease types
    
    # Paths
    DATA_DIR = './data'
    CHECKPOINT_DIR = './checkpoints'
    LOG_DIR = './logs'
    ML_DIR = './ml'
