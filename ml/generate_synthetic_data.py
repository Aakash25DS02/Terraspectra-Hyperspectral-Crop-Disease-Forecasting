import numpy as np
import h5py
import os
from tqdm import tqdm
import matplotlib.pyplot as plt

class SyntheticHyperspectralDataGenerator:
    def __init__(self, patch_size=64, num_bands=100, num_samples=1000):
        self.patch_size = patch_size
        self.num_bands = num_bands
        self.num_samples = num_samples
        
        # Define spectral bands (400-1000nm range)
        self.wavelengths = np.linspace(400, 1000, num_bands)
        
    def generate_healthy_spectrum(self):
        """Generate typical healthy vegetation spectral signature"""
        spectrum = np.zeros(self.num_bands)
        
        # Green peak (around 550nm)
        green_peak = np.exp(-((self.wavelengths - 550) ** 2) / (2 * 20 ** 2))
        spectrum += 0.8 * green_peak
        
        # Red edge (700-750nm) - sharp increase
        red_edge = 1 / (1 + np.exp(-(self.wavelengths - 720) / 10))
        spectrum += 0.6 * red_edge
        
        # NIR plateau (750-1300nm) - high reflectance
        nir_plateau = 0.7 * np.ones(self.num_bands)
        nir_plateau[self.wavelengths < 750] = 0
        spectrum += nir_plateau
        
        # Water absorption bands
        water_bands = [970, 1130, 1450]
        for band in water_bands:
            if band >= 400 and band <= 1000:
                idx = np.argmin(np.abs(self.wavelengths - band))
                spectrum[max(0, idx-5):min(self.num_bands, idx+5)] *= 0.3
        
        # Add some noise
        spectrum += np.random.normal(0, 0.02, self.num_bands)
        spectrum = np.clip(spectrum, 0, 1)
        
        return spectrum
    
    def generate_diseased_spectrum(self, disease_type='fungal'):
        """Generate diseased vegetation spectral signature"""
        healthy = self.generate_healthy_spectrum()
        
        if disease_type == 'fungal':
            healthy[20:40] *= 0.6  # Reduce green peak
            healthy[60:80] *= 0.7  # Reduce red edge
            healthy[80:] *= 0.8    # Reduce NIR
            
        elif disease_type == 'bacterial':
            healthy *= 0.6
            healthy[90:] *= 0.4  # Strong water absorption
            
        elif disease_type == 'viral':
            mask = np.random.random(self.num_bands) > 0.7
            healthy[mask] *= 0.3
        
        # Add disease-specific noise
        healthy += np.random.normal(0, 0.05, self.num_bands)
        healthy = np.clip(healthy, 0, 1)
        
        return healthy
    
    def create_patch_with_disease(self, base_spectrum, disease_mask, disease_type):
        """Create a patch with disease patterns"""
        patch = np.zeros((self.patch_size, self.patch_size, self.num_bands))
        
        # Start with healthy spectrum everywhere
        for i in range(self.patch_size):
            for j in range(self.patch_size):
                patch[i, j] = base_spectrum.copy()
        
        # Apply disease to masked regions
        diseased_spectrum = self.generate_diseased_spectrum(disease_type)
        
        for i in range(self.patch_size):
            for j in range(self.patch_size):
                if disease_mask[i, j]:
                    blend_ratio = disease_mask[i, j]
                    patch[i, j] = (1 - blend_ratio) * base_spectrum + blend_ratio * diseased_spectrum
        
        return patch
    
    def generate_disease_mask(self, disease_coverage=0.3):
        """Generate a mask showing where disease is present"""
        mask = np.zeros((self.patch_size, self.patch_size))
        
        # Create random disease patches
        num_patches = np.random.randint(1, 4)
        
        for _ in range(num_patches):
            x = np.random.randint(0, self.patch_size - 10)
            y = np.random.randint(0, self.patch_size - 10)
            w = np.random.randint(5, 15)
            h = np.random.randint(5, 15)
            severity = np.random.uniform(0.3, 1.0)
            mask[x:x+h, y:y+w] = severity
        
        return mask
    
    def generate_dataset(self, save_dir="./data/synthetic"):
        """Generate complete synthetic dataset"""
        os.makedirs(save_dir, exist_ok=True)
        
        classes = ['healthy', 'fungal', 'bacterial', 'viral', 'nutrient_deficiency']
        
        X = []  # Images
        y = []  # Labels
        
        print(f"Generating {self.num_samples} synthetic samples...")
        
        for i in tqdm(range(self.num_samples)):
            class_idx = np.random.randint(0, len(classes))
            class_name = classes[class_idx]
            
            if class_name == 'healthy':
                base_spectrum = self.generate_healthy_spectrum()
                disease_mask = np.zeros((self.patch_size, self.patch_size))
            else:
                base_spectrum = self.generate_healthy_spectrum()
                disease_mask = self.generate_disease_mask()
            
            patch = self.create_patch_with_disease(base_spectrum, disease_mask, class_name)
            patch += np.random.normal(0, 0.01, patch.shape)
            patch = np.clip(patch, 0, 1)
            
            X.append(patch)
            y.append(class_idx)
        
        X = np.array(X, dtype=np.float32)
        y = np.array(y, dtype=np.int64)
        
        # Save as HDF5
        with h5py.File(os.path.join(save_dir, 'synthetic_data.h5'), 'w') as f:
            f.create_dataset('images', data=X)
            f.create_dataset('labels', data=y)
            f.create_dataset('wavelengths', data=self.wavelengths)
        
        # Save class names
        with open(os.path.join(save_dir, 'class_names.txt'), 'w') as f:
            for i, name in enumerate(classes):
                f.write(f"{i}: {name}\n")
        
        print(f"Dataset saved to {save_dir}")
        print(f"Images shape: {X.shape}")
        print(f"Labels shape: {y.shape}")
        
        return X, y, classes
    
    def visualize_sample(self, X, y, classes, sample_idx=0):
        """Visualize a sample from the dataset"""
        sample = X[sample_idx]
        label = y[sample_idx]
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # RGB approximation
        rgb = np.stack([sample[:, :, 40], sample[:, :, 50], sample[:, :, 60]], axis=-1)
        rgb = np.clip(rgb, 0, 1)
        
        axes[0].imshow(rgb)
        axes[0].set_title(f'RGB Approximation\nClass: {classes[label]}')
        axes[0].axis('off')
        
        # Spectral signature of center pixel
        center_pixel = sample[32, 32, :]
        axes[1].plot(self.wavelengths, center_pixel)
        axes[1].set_title('Spectral Signature (Center Pixel)')
        axes[1].set_xlabel('Wavelength (nm)')
        axes[1].set_ylabel('Reflectance')
        axes[1].grid(True)
        
        # Mean spectral signature
        mean_spectrum = np.mean(sample, axis=(0, 1))
        axes[2].plot(self.wavelengths, mean_spectrum)
        axes[2].set_title('Mean Spectral Signature')
        axes[2].set_xlabel('Wavelength (nm)')
        axes[2].set_ylabel('Reflectance')
        axes[2].grid(True)
        
        plt.tight_layout()
        plt.savefig(f'./data/synthetic/sample_{sample_idx}.png')
        plt.close()
        
        print(f"Visualization saved for sample {sample_idx}")

def main():
    generator = SyntheticHyperspectralDataGenerator(
        patch_size=64,
        num_bands=100,
        num_samples=500
    )
    
    X, y, classes = generator.generate_dataset()
    
    for i in range(3):
        generator.visualize_sample(X, y, classes, sample_idx=i)
    
    print("Data generation complete!")
    print(f"Classes: {classes}")
    print(f"Class distribution: {np.bincount(y)}")

if __name__ == "__main__":
    main()


