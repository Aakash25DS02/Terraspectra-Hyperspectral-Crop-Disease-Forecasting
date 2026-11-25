import torch
import torch.nn as nn
import torch.nn.functional as F

class HyperspectralCNN3D(nn.Module):
    """
    3D CNN for Hyperspectral Image Classification
    
    Input: (batch_size, channels, depth, height, width)
    For hyperspectral: channels=1, depth=num_bands, height=patch_size, width=patch_size
    """
    
    def __init__(self, num_classes=5, num_bands=100, patch_size=64):
        super(HyperspectralCNN3D, self).__init__()
        
        self.num_bands = num_bands
        self.patch_size = patch_size
        
        # First 3D Convolutional Block
        self.conv1 = nn.Conv3d(
            in_channels=1, 
            out_channels=32, 
            kernel_size=(3, 3, 3), 
            stride=1, 
            padding=1
        )
        self.bn1 = nn.BatchNorm3d(32)
        self.relu1 = nn.ReLU(inplace=True)
        self.pool1 = nn.MaxPool3d(kernel_size=(2, 2, 2), stride=2)
        
        # Second 3D Convolutional Block
        self.conv2 = nn.Conv3d(
            in_channels=32, 
            out_channels=64, 
            kernel_size=(3, 3, 3), 
            stride=1, 
            padding=1
        )
        self.bn2 = nn.BatchNorm3d(64)
        self.relu2 = nn.ReLU(inplace=True)
        self.pool2 = nn.MaxPool3d(kernel_size=(2, 2, 2), stride=2)
        
        # Third 3D Convolutional Block
        self.conv3 = nn.Conv3d(
            in_channels=64, 
            out_channels=128, 
            kernel_size=(3, 3, 3), 
            stride=1, 
            padding=1
        )
        self.bn3 = nn.BatchNorm3d(128)
        self.relu3 = nn.ReLU(inplace=True)
        self.pool3 = nn.MaxPool3d(kernel_size=(2, 2, 2), stride=2)
        
        # Calculate the size after convolutions
        # After 3 max pooling operations with kernel_size=2, dimensions are divided by 8
        self.feature_size = 128 * (num_bands // 8) * (patch_size // 8) * (patch_size // 8)
        
        # Fully Connected Layers
        self.fc1 = nn.Linear(self.feature_size, 512)
        self.dropout1 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(512, 256)
        self.dropout2 = nn.Dropout(0.5)
        self.fc3 = nn.Linear(256, num_classes)
        
    def forward(self, x):
        """
        Forward pass
        
        Args:
            x: Input tensor of shape (batch_size, 1, num_bands, patch_size, patch_size)
        """
        
        # First Conv Block
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu1(x)
        x = self.pool1(x)
        
        # Second Conv Block
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu2(x)
        x = self.pool2(x)
        
        # Third Conv Block
        x = self.conv3(x)
        x = self.bn3(x)
        x = self.relu3(x)
        x = self.pool3(x)
        
        # Flatten
        x = x.view(x.size(0), -1)
        
        # Fully Connected Layers
        x = F.relu(self.fc1(x))
        x = self.dropout1(x)
        x = F.relu(self.fc2(x))
        x = self.dropout2(x)
        x = self.fc3(x)
        
        return x

class HyperspectralCNN3D_Simplified(nn.Module):
    """
    Simplified 3D CNN for faster training and testing
    """
    
    def __init__(self, num_classes=5, num_bands=100, patch_size=64):
        super(HyperspectralCNN3D_Simplified, self).__init__()
        
        self.conv1 = nn.Conv3d(1, 16, kernel_size=(3, 3, 3), padding=1)
        self.bn1 = nn.BatchNorm3d(16)
        self.pool1 = nn.MaxPool3d(kernel_size=(2, 2, 2))
        
        self.conv2 = nn.Conv3d(16, 32, kernel_size=(3, 3, 3), padding=1)
        self.bn2 = nn.BatchNorm3d(32)
        self.pool2 = nn.MaxPool3d(kernel_size=(2, 2, 2))
        
        self.conv3 = nn.Conv3d(32, 64, kernel_size=(3, 3, 3), padding=1)
        self.bn3 = nn.BatchNorm3d(64)
        self.pool3 = nn.MaxPool3d(kernel_size=(2, 2, 2))
        
        # Calculate feature size
        self.feature_size = 64 * (num_bands // 8) * (patch_size // 8) * (patch_size // 8)
        
        self.fc1 = nn.Linear(self.feature_size, 128)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(128, num_classes)
        
    def forward(self, x):
        x = self.pool1(F.relu(self.bn1(self.conv1(x))))
        x = self.pool2(F.relu(self.bn2(self.conv2(x))))
        x = self.pool3(F.relu(self.bn3(self.conv3(x))))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

def test_model():
    """Test the model with dummy input"""
    
    # Model parameters
    batch_size = 2
    num_bands = 100
    patch_size = 64
    num_classes = 5
    
    # Create dummy input (batch_size, 1, num_bands, patch_size, patch_size)
    dummy_input = torch.randn(batch_size, 1, num_bands, patch_size, patch_size)
    
    print(f"Input shape: {dummy_input.shape}")
    
    # Test full model
    model = HyperspectralCNN3D(num_classes=num_classes, num_bands=num_bands, patch_size=patch_size)
    output = model(dummy_input)
    
    print(f"Full model output shape: {output.shape}")
    print(f"Full model parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    # Test simplified model
    model_simple = HyperspectralCNN3D_Simplified(num_classes=num_classes, num_bands=num_bands, patch_size=patch_size)
    output_simple = model_simple(dummy_input)
    
    print(f"Simplified model output shape: {output_simple.shape}")
    print(f"Simplified model parameters: {sum(p.numel() for p in model_simple.parameters()):,}")
    
    return model, model_simple

if __name__ == "__main__":
    test_model()