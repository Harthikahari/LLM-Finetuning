#!/usr/bin/env python3
"""
Evaluation script for Text2SQL models.

Example usage:
    python scripts/evaluate.py --model ./outputs --dataset spider --split test
"""

import argparse
import logging
import json
from pathlib import Path

from text2sql.utils.logging import setup_logging
from text2sql.data.datasets import load_dataset
from text2sql.models.model_factory import create_model
from text2sql.evaluation.evaluator import evaluate_model


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate Text2SQL model")

    parser.add_argument("--model", type=str, required=True, help="Model path")
    parser.add_argument("--dataset", type=str, required=True, help="Dataset name")
    parser.add_argument("--split", type=str, default="test", choices=["train", "validation", "test"])
    parser.add_argument("--output_file", type=str, default="evaluation_results.json")
    parser.add_argument("--batch_size", type=int, default=1)
    parser.add_argument("--max_new_tokens", type=int, default=256)

    return parser.parse_args()


def main():
    args = parse_args()

    # Setup logging
    setup_logging(level="INFO")
    logger = logging.getLogger(__name__)

    logger.info("Starting Text2SQL evaluation")
    logger.info(f"Arguments: {args}")

    # Load dataset
    logger.info(f"Loading dataset: {args.dataset}, split: {args.split}")
    eval_examples = load_dataset(args.dataset, split=args.split)
    logger.info(f"Loaded {len(eval_examples)} examples")

    # Load model
    logger.info(f"Loading model from {args.model}")
    model = create_model(
        model_name=args.model,
        training_method="lora",  # Assumes LoRA adapter
    )

    # Evaluate
    logger.info("Running evaluation")
    results = evaluate_model(
        model=model,
        tokenizer=model.tokenizer,
        eval_dataset=eval_examples,
        max_new_tokens=args.max_new_tokens,
        batch_size=args.batch_size,
    )

    # Save results
    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    logger.info(f"Results saved to {output_path}")
    logger.info("Evaluation results:")
    for metric, value in results.items():
        logger.info(f"  {metric}: {value:.4f}")


if __name__ == "__main__":
    main()
