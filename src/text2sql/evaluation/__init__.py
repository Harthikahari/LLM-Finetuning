"""Evaluation framework for Text2SQL models."""

from text2sql.evaluation.evaluator import Text2SQLEvaluator, evaluate_model
from text2sql.evaluation.sql_executor import SQLExecutor, execute_sql
from text2sql.evaluation.benchmarks import run_benchmark, BENCHMARKS

__all__ = [
    "Text2SQLEvaluator",
    "evaluate_model",
    "SQLExecutor",
    "execute_sql",
    "run_benchmark",
    "BENCHMARKS",
]
