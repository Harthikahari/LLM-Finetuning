"""Helper utilities for Text2SQL."""

import logging
import random
import numpy as np
import torch

logger = logging.getLogger(__name__)


def set_seed(seed: int = 42):
    """Set random seed for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    logger.info(f"Random seed set to {seed}")


def get_device() -> str:
    """Get available device."""
    if torch.cuda.is_available():
        device = "cuda"
        logger.info(f"Using CUDA: {torch.cuda.get_device_name(0)}")
    else:
        device = "cpu"
        logger.info("Using CPU")
    return device


def count_parameters(model) -> int:
    """Count total parameters in model."""
    return sum(p.numel() for p in model.parameters())


def get_gpu_memory():
    """Get GPU memory usage."""
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated() / 1024**3
        reserved = torch.cuda.memory_reserved() / 1024**3
        logger.info(f"GPU Memory - Allocated: {allocated:.2f}GB, Reserved: {reserved:.2f}GB")
        return {"allocated": allocated, "reserved": reserved}
    return None
