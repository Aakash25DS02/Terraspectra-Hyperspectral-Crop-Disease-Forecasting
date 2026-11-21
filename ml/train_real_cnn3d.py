
from pathlib import Path
import random
import sys

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cnn3d import HyperspectralCNN3D_Simplified
from dataset.real_data_loader import RealHyperspectralDataset

# Training configuration
SEED = 42
EPOCHS = 20
BATCH_SIZE = 4
LEARNING_RATE = 0.0001

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

# Use Apple GPU when available
device = torch.device(
    "mps" if torch.backends.mps.is_available() else "cpu"
)

# Load real hyperspectral dataset
root = Path("data/real/kaggle_2026")

train_dataset = RealHyperspectralDataset(
    root / "train_manifest.csv"
)

val_dataset = RealHyperspectralDataset(
    root / "val_manifest.csv"
)

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)

# Initialize 3D-CNN for real wheat images
model = HyperspectralCNN3D_Simplified(
    num_classes=3,
    num_bands=125,
    patch_size=32
).to(device)

criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE
)

# Save best model checkpoint
checkpoint_dir = Path("checkpoints/real")
checkpoint_dir.mkdir(parents=True, exist_ok=True)

checkpoint_path = (
    checkpoint_dir / "cnn3d_wheat_20epochs_best.pth"
)

best_val_accuracy = -1.0
best_epoch = 0

print("TERRASPECTRA REAL 3D-CNN TRAINING")
print("--------------------------------")
print("Device:", device)
print("Training images:", len(train_dataset))
print("Validation images:", len(val_dataset))
print("Epochs:", EPOCHS)
print("Batch size:", BATCH_SIZE)
print("Learning rate:", LEARNING_RATE)

# Training loop
for epoch in range(EPOCHS):

    model.train()

    train_loss = 0.0
    train_correct = 0
    train_total = 0

    for images, labels in train_loader:

        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad(set_to_none=True)

        outputs = model(images)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        train_loss += loss.item() * labels.size(0)

        train_correct += (
            outputs.argmax(dim=1) == labels
        ).sum().item()

        train_total += labels.size(0)

    # Validation loop
    model.eval()

    val_loss = 0.0
    val_correct = 0
    val_total = 0

    with torch.no_grad():

        for images, labels in val_loader:

            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)

            val_loss += loss.item() * labels.size(0)

            val_correct += (
                outputs.argmax(dim=1) == labels
            ).sum().item()

            val_total += labels.size(0)

    train_accuracy = train_correct / train_total
    val_accuracy = val_correct / val_total

    avg_train_loss = train_loss / train_total
    avg_val_loss = val_loss / val_total

    print(
        f"Epoch {epoch + 1}/{EPOCHS} | "
        f"Train Loss: {avg_train_loss:.4f} | "
        f"Train Acc: {train_accuracy:.4f} | "
        f"Val Loss: {avg_val_loss:.4f} | "
        f"Val Acc: {val_accuracy:.4f}",
        flush=True
    )

    # Save checkpoint when validation accuracy improves
    if val_accuracy > best_val_accuracy:

        best_val_accuracy = val_accuracy
        best_epoch = epoch + 1

        torch.save({
            "model_state_dict": model.state_dict(),
            "num_classes": 3,
            "num_bands": 125,
            "patch_size": 32,
            "class_names": ["Healthy", "Rust", "Other"],
            "normalization": "divide_by_65535",
            "epoch": best_epoch,
            "val_accuracy": val_accuracy,
        }, checkpoint_path)

        print(
            "Best checkpoint saved:",
            checkpoint_path,
            flush=True
        )

print("\nTRAINING COMPLETED")
print("Best epoch:", best_epoch)
print("Best validation accuracy:", round(best_val_accuracy, 4))
print("Checkpoint:", checkpoint_path)
