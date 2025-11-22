#!/usr/bin/env python3
"""
Script to download and prepare datasets.

Example usage:
    python scripts/download_data.py --dataset spider --output_dir ./data
"""

import argparse
import logging
from pathlib import Path

from text2sql.utils.logging import setup_logging
from text2sql.data.datasets import load_dataset


def parse_args():
    parser = argparse.ArgumentParser(description="Download Text2SQL datasets")

    parser.add_argument("--dataset", type=str, required=True, help="Dataset name")
    parser.add_argument("--output_dir", type=str, default="./data")
    parser.add_argument("--splits", nargs="+", default=["train", "validation", "test"])

    return parser.parse_args()


def main():
    args = parse_args()

    # Setup logging
    setup_logging(level="INFO")
    logger = logging.getLogger(__name__)

    logger.info(f"Downloading dataset: {args.dataset}")

    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Download each split
    for split in args.splits:
        logger.info(f"Downloading {split} split")
        try:
            data = load_dataset(
                dataset_name=args.dataset,
                split=split,
                cache_dir=str(output_path / "cache"),
            )
            logger.info(f"Downloaded {len(data)} examples for {split} split")
        except Exception as e:
            logger.error(f"Failed to download {split} split: {e}")

    logger.info("Download completed")


if __name__ == "__main__":
    main()
