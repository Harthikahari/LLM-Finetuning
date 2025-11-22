"""
Text2SQL: A production-grade fine-tuning framework for Text-to-SQL generation.

This package provides a comprehensive solution for training, evaluating, and deploying
Large Language Models for converting natural language queries to SQL.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__license__ = "MIT"

from text2sql.data import datasets, preprocessing, tokenization
from text2sql.models import model_factory
from text2sql.training import trainer
from text2sql.evaluation import evaluator
from text2sql.inference import predictor

__all__ = [
    "datasets",
    "preprocessing",
    "tokenization",
    "model_factory",
    "trainer",
    "evaluator",
    "predictor",
]
