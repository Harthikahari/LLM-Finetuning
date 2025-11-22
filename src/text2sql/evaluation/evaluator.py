"""Evaluator for Text2SQL models."""

import logging
from typing import List, Dict, Any, Optional
import numpy as np
from tqdm import tqdm

logger = logging.getLogger(__name__)


class Text2SQLEvaluator:
    """Evaluator for Text2SQL models."""

    def __init__(
        self,
        model,
        tokenizer,
        metrics: Optional[List[str]] = None,
    ):
        self.model = model
        self.tokenizer = tokenizer
        self.metrics = metrics or ["exact_match", "execution_accuracy"]

    def evaluate(
        self,
        examples: List,
        max_new_tokens: int = 256,
        batch_size: int = 1,
    ) -> Dict[str, Any]:
        """Evaluate model on examples."""
        predictions = []
        references = []

        logger.info(f"Evaluating on {len(examples)} examples")

        for example in tqdm(examples, desc="Evaluating"):
            # Generate prediction
            pred = self.model.generate(
                example.question,
                max_new_tokens=max_new_tokens,
            )[0]

            predictions.append(pred)
            references.append(example.query)

        # Compute metrics
        results = self._compute_metrics(predictions, references)

        logger.info("Evaluation results:")
        for metric, value in results.items():
            logger.info(f"  {metric}: {value:.4f}")

        return results

    def _compute_metrics(
        self,
        predictions: List[str],
        references: List[str],
    ) -> Dict[str, float]:
        """Compute evaluation metrics."""
        from text2sql.training.metrics import exact_match_score

        metrics = {}

        if "exact_match" in self.metrics:
            metrics["exact_match"] = exact_match_score(predictions, references)

        if "execution_accuracy" in self.metrics:
            # Placeholder for execution accuracy
            metrics["execution_accuracy"] = 0.0

        return metrics


def evaluate_model(model, tokenizer, eval_dataset, **kwargs) -> Dict[str, float]:
    """Convenience function to evaluate a model."""
    evaluator = Text2SQLEvaluator(model, tokenizer)
    return evaluator.evaluate(eval_dataset, **kwargs)
