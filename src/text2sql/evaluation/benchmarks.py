"""Benchmark datasets for Text2SQL evaluation."""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

BENCHMARKS = {
    "spider": {"name": "Spider", "size": 10181},
    "wikisql": {"name": "WikiSQL", "size": 80654},
    "bird": {"name": "BIRD", "size": 12751},
}


def run_benchmark(model, tokenizer, benchmark_name: str, **kwargs) -> Dict:
    """Run model on benchmark dataset."""
    from text2sql.data.datasets import load_dataset
    from text2sql.evaluation.evaluator import evaluate_model

    logger.info(f"Running benchmark: {benchmark_name}")

    # Load benchmark data
    test_data = load_dataset(benchmark_name, split="test", **kwargs)

    # Evaluate
    results = evaluate_model(model, tokenizer, test_data)

    results["benchmark"] = benchmark_name
    return results
