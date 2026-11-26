import torch
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

DEFAULT_CHECKPOINT = (
    ROOT / "checkpoints/real/"
    "cnn3d_wheat_standardized_best.pth"
)


def load_pretrained_cnn(
    model,
    checkpoint_path=DEFAULT_CHECKPOINT,
):
    """
    Transfer pretrained CNN feature extraction
    weights into the hybrid CNN-ViT model.
    """

    checkpoint_path = Path(checkpoint_path)

    if not checkpoint_path.is_file():
        raise FileNotFoundError(
            f"Checkpoint not found: {checkpoint_path}"
        )

    checkpoint = torch.load(
        checkpoint_path,
        map_location="cpu",
        weights_only=False,
    )

    if checkpoint.get("normalization") != "per_band":
        raise ValueError(
            "Expected a per-band standardized checkpoint."
        )

    source_state = checkpoint["model_state_dict"]

    target_state = model.cnn.state_dict()

    transferred_state = {}

    for name, target_tensor in target_state.items():

        if name not in source_state:
            raise KeyError(
                f"Missing pretrained parameter: {name}"
            )

        source_tensor = source_state[name]

        if source_tensor.shape != target_tensor.shape:
            raise ValueError(
                f"Shape mismatch for {name}: "
                f"{source_tensor.shape} vs "
                f"{target_tensor.shape}"
            )

        if source_tensor.dtype != target_tensor.dtype:
            raise ValueError(
                f"Data type mismatch for {name}"
            )

        if not torch.isfinite(source_tensor).all():
            raise ValueError(
                f"Non-finite values in {name}"
            )

        transferred_state[name] = source_tensor

    model.cnn.load_state_dict(
        transferred_state,
        strict=True,
    )

    for name, tensor in model.cnn.state_dict().items():

        torch.testing.assert_close(
            tensor.detach().cpu(),
            transferred_state[name].cpu(),
            atol=0,
            rtol=0,
        )

    skipped_keys = sorted(
        set(source_state) - set(target_state)
    )

    print("Pretrained CNN weights loaded successfully!")

    print(
        f"Transferred state entries: "
        f"{len(transferred_state)}"
    )

    print(
        f"Skipped classifier entries: "
        f"{len(skipped_keys)}"
    )

    for name in skipped_keys:
        print(f"  Skipped: {name}")

    print("Exact weight verification: PASSED")

    return checkpoint
