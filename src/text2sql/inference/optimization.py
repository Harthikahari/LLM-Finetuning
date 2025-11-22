"""Model optimization for inference."""

import logging
import torch

logger = logging.getLogger(__name__)


def optimize_model(model, optimization_type: str = "bettertransformer"):
    """Optimize model for inference."""
    logger.info(f"Optimizing model with: {optimization_type}")

    if optimization_type == "bettertransformer":
        try:
            from optimum.bettertransformer import BetterTransformer
            model = BetterTransformer.transform(model)
            logger.info("Applied BetterTransformer optimization")
        except ImportError:
            logger.warning("optimum not installed. Install with: pip install optimum")

    return model


def quantize_model(model, quantization_type: str = "int8"):
    """Quantize model for deployment."""
    logger.info(f"Quantizing model to: {quantization_type}")

    if quantization_type == "int8":
        model = torch.quantization.quantize_dynamic(
            model, {torch.nn.Linear}, dtype=torch.qint8
        )
        logger.info("Applied INT8 quantization")

    return model
