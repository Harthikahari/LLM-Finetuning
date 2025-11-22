"""Learning rate schedulers for Text2SQL training."""

import logging
from typing import Optional
from transformers import get_scheduler as hf_get_scheduler

logger = logging.getLogger(__name__)


def get_scheduler(
    name: str,
    optimizer,
    num_warmup_steps: int = 0,
    num_training_steps: int = 1000,
    **kwargs,
):
    """
    Get learning rate scheduler.

    Args:
        name: Scheduler name (linear, cosine, cosine_with_restarts, polynomial, constant, constant_with_warmup)
        optimizer: Optimizer instance
        num_warmup_steps: Number of warmup steps
        num_training_steps: Total number of training steps
        **kwargs: Additional scheduler arguments

    Returns:
        Scheduler instance
    """
    logger.info(f"Creating {name} scheduler with {num_warmup_steps} warmup steps")

    scheduler = hf_get_scheduler(
        name=name,
        optimizer=optimizer,
        num_warmup_steps=num_warmup_steps,
        num_training_steps=num_training_steps,
        **kwargs,
    )

    return scheduler
