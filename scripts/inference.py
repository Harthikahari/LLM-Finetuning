#!/usr/bin/env python3
"""
Inference script for Text2SQL models.

Example usage:
    python scripts/inference.py --model ./outputs --question "What are all employee names?"
"""

import argparse
import logging

from text2sql.utils.logging import setup_logging
from text2sql.models.model_factory import create_model
from text2sql.inference.predictor import Text2SQLPredictor


def parse_args():
    parser = argparse.ArgumentParser(description="Run inference with Text2SQL model")

    parser.add_argument("--model", type=str, required=True, help="Model path")
    parser.add_argument("--question", type=str, required=True, help="Natural language question")
    parser.add_argument("--schema", type=str, help="Database schema")
    parser.add_argument("--max_new_tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--num_return_sequences", type=int, default=1)

    return parser.parse_args()


def main():
    args = parse_args()

    # Setup logging
    setup_logging(level="INFO")
    logger = logging.getLogger(__name__)

    logger.info("Starting Text2SQL inference")

    # Load model
    logger.info(f"Loading model from {args.model}")
    model = create_model(
        model_name=args.model,
        training_method="lora",
    )

    # Create predictor
    predictor = Text2SQLPredictor(
        model=model,
        tokenizer=model.tokenizer,
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature,
    )

    # Run prediction
    logger.info(f"Question: {args.question}")
    queries = predictor.predict(
        question=args.question,
        schema=args.schema,
        num_return_sequences=args.num_return_sequences,
    )

    # Print results
    print("\n" + "=" * 80)
    print("Generated SQL Queries:")
    print("=" * 80)
    for i, query in enumerate(queries, 1):
        print(f"\nQuery {i}:")
        print(query)
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
