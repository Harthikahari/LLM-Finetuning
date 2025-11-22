#!/usr/bin/env python3
"""
Data preparation pipeline.

Example usage:
    python scripts/prepare_data.py --dataset spider --output_dir ./data/prepared
"""

import argparse
import logging
import json
from pathlib import Path

from text2sql.utils.logging import setup_logging
from text2sql.data.datasets import load_dataset
from text2sql.data.preprocessing import preprocess_data


def parse_args():
    parser = argparse.ArgumentParser(description="Prepare Text2SQL dataset")

    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--output_dir", type=str, default="./data/prepared")
    parser.add_argument("--clean_queries", action="store_true", default=True)
    parser.add_argument("--normalize_schemas", action="store_true", default=True)

    return parser.parse_args()


def main():
    args = parse_args()

    setup_logging(level="INFO")
    logger = logging.getLogger(__name__)

    logger.info("Preparing dataset")

    # Load dataset
    train_data = load_dataset(args.dataset, split="train")
    eval_data = load_dataset(args.dataset, split="validation")

    # Preprocess
    train_data = preprocess_data(
        train_data,
        clean_queries=args.clean_queries,
        normalize_schemas=args.normalize_schemas,
    )

    eval_data = preprocess_data(
        eval_data,
        clean_queries=args.clean_queries,
        normalize_schemas=args.normalize_schemas,
    )

    # Save
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(output_path / "train.json", "w") as f:
        json.dump([ex.to_dict() for ex in train_data], f, indent=2)

    with open(output_path / "eval.json", "w") as f:
        json.dump([ex.to_dict() for ex in eval_data], f, indent=2)

    logger.info(f"Prepared data saved to {output_path}")


if __name__ == "__main__":
    main()
