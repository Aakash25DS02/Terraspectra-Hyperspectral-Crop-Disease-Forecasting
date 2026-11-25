import torch
import torch.nn as nn

class SpatialSpectralTokenEmbedding(nn.Module):
    """
    Converts 5D 3D-CNN feature maps (Batch, Channels, Depth, Height, Width)
    into a sequence of tokens (Batch, Num_Tokens, Embed_Dim) for Transformer processing.
    """
    def __init__(self, in_channels=128, embed_dim=256, max_tokens=1000):
        super(SpatialSpectralTokenEmbedding, self).__init__()
        
        self.embed_dim = embed_dim
        # Projection layer to map CNN features to Transformer embedding dimension
        self.proj = nn.Linear(in_channels, embed_dim)
        
        # Learnable positional embeddings
        self.pos_embedding = nn.Parameter(torch.zeros(1, max_tokens, embed_dim))
        nn.init.trunc_normal_(self.pos_embedding, std=0.02)

    def forward(self, x):
        """
        Args:
            x: Tensor of shape (B, C, D, H, W) from 3D-CNN feature extractor
        Returns:
            tokens: Tensor of shape (B, N, embed_dim) ready for ViT
        """
        B, C, D, H, W = x.shape
        
        # Rearrange from (B, C, D, H, W) -> (B, D, H, W, C) -> (B, D*H*W, C)
        x = x.permute(0, 2, 3, 4, 1)
        x = x.reshape(B, D * H * W, C)
        
        # Project channel dimension to embed_dim: (B, N, embed_dim)
        tokens = self.proj(x)
        
        # Add positional embedding
        num_tokens = tokens.shape[1]
        tokens = tokens + self.pos_embedding[:, :num_tokens, :]
        
        return tokens

def test_token_embedding():
    # Example 5D feature tensor from a 3D-CNN layer:
    # Batch size = 2, Channels = 128, Depth (spectral) = 12, Height = 8, Width = 8
    dummy_cnn_features = torch.randn(2, 128, 12, 8, 8)
    
    embedder = SpatialSpectralTokenEmbedding(in_channels=128, embed_dim=256)
    tokens = embedder(dummy_cnn_features)
    
    print("Input CNN Feature Map Shape:", dummy_cnn_features.shape)
    print("Output Token Sequence Shape:", tokens.shape)
    print("Expected Token Count (D*H*W):", 12 * 8 * 8)
    assert tokens.shape == (2, 768, 256), "Shape mismatch in Token Embedding module!"
    print("Token Embedding test passed successfully!")

if __name__ == "__main__":
    test_token_embedding()