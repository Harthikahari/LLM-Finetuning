#!/usr/bin/env python3
"""
Benchmark script for performance testing.

Example usage:
    python scripts/benchmark.py --model ./outputs --benchmark spider
"""

import argparse
import logging

from text2sql.utils.logging import setup_logging
from text2sql.models.model_factory import create_model
from text2sql.evaluation.benchmarks import run_benchmark


def parse_args():
    parser = argparse.ArgumentParser(description="Run benchmark")

    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--benchmark", type=str, required=True, choices=["spider", "wikisql", "bird"])

    return parser.parse_args()


def main():
    args = parse_args()

    setup_logging(level="INFO")
    logger = logging.getLogger(__name__)

    logger.info(f"Running benchmark: {args.benchmark}")

    # Load model
    model = create_model(args.model, training_method="lora")

    # Run benchmark
    results = run_benchmark(
        model=model,
        tokenizer=model.tokenizer,
        benchmark_name=args.benchmark,
    )

    logger.info(f"Benchmark results: {results}")


if __name__ == "__main__":
    main()
