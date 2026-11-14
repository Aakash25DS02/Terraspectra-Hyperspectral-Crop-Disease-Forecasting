# Create data loader script
import h5py
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import os

class HyperspectralDataset(Dataset):
    def __init__(self, data_path, transform=None):
        self.data_path = data_path
        self.transform = transform
        
        with h5py.File(data_path, 'r') as f:
            self.images = f['images'][:]
            self.labels = f['labels'][:]
            self.wavelengths = f['wavelengths'][:]
        
        class_file = os.path.join(os.path.dirname(data_path), 'class_names.txt')
        self.class_names = {}
        with open(class_file, 'r') as f:
            for line in f:
                idx, name = line.strip().split(': ')
                self.class_names[int(idx)] = name
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        image = self.images[idx]
        label = self.labels[idx]
        
        image = torch.from_numpy(image).permute(2, 0, 1).float()
        label = torch.tensor(label, dtype=torch.long)
        
        if self.transform:
            image = self.transform(image)
        
        return image, label
    
    def get_class_name(self, label_idx):
        return self.class_names[label_idx]

def create_data_loaders(batch_size=32, num_workers=4):
    train_path = "./data/synthetic/synthetic_data.h5"
    
    train_dataset = HyperspectralDataset(train_path)
    
    dataset_size = len(train_dataset)
    train_size = int(0.8 * dataset_size)
    val_size = dataset_size - train_size
    
    train_subset, val_subset = torch.utils.data.random_split(
        train_dataset, [train_size, val_size]
    )
    
    train_loader = DataLoader(
        train_subset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )
    
    val_loader = DataLoader(
        val_subset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    return train_loader, val_loader, train_dataset.class_names

def main():
    train_loader, val_loader, class_names = create_data_loaders()
    
    print(f"Class names: {class_names}")
    print(f"Train batches: {len(train_loader)}")
    print(f"Validation batches: {len(val_loader)}")
    
    for batch_idx, (images, labels) in enumerate(train_loader):
        print(f"Batch {batch_idx}:")
        print(f"  Images shape: {images.shape}")
        print(f"  Labels shape: {labels.shape}")
        print(f"  Labels: {labels}")
        
        if batch_idx == 0:
            break

if __name__ == "__main__":
    main()