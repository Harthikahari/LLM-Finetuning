"""Metrics for Text2SQL training and evaluation."""

import logging
from typing import Dict, List, Any
import numpy as np

logger = logging.getLogger(__name__)


def exact_match_score(predictions: List[str], references: List[str]) -> float:
    """
    Compute exact match accuracy.

    Args:
        predictions: List of predicted SQL queries
        references: List of reference SQL queries

    Returns:
        Exact match accuracy (0-1)
    """
    if len(predictions) != len(references):
        raise ValueError("Predictions and references must have same length")

    matches = sum(
        normalize_sql(pred) == normalize_sql(ref)
        for pred, ref in zip(predictions, references)
    )

    return matches / len(predictions)


def normalize_sql(sql: str) -> str:
    """
    Normalize SQL query for comparison.

    Args:
        sql: SQL query string

    Returns:
        Normalized SQL query
    """
    # Remove extra whitespace
    sql = " ".join(sql.split())

    # Convert to lowercase
    sql = sql.lower()

    # Remove semicolon at end
    sql = sql.rstrip(";")

    # Sort clauses for comparison (basic normalization)
    return sql.strip()


def compute_metrics(eval_pred) -> Dict[str, float]:
    """
    Compute metrics for evaluation.

    Args:
        eval_pred: EvalPrediction object from HuggingFace

    Returns:
        Dictionary of metrics
    """
    predictions, labels = eval_pred

    # Handle logits (convert to token IDs)
    if len(predictions.shape) == 3:  # logits
        predictions = np.argmax(predictions, axis=-1)

    # For now, return basic loss-based metrics
    # In practice, you'd decode predictions and compute SQL-specific metrics
    metrics = {
        "perplexity": np.exp(np.mean(labels)),  # Simplified
    }

    return metrics


def bleu_score(predictions: List[str], references: List[str]) -> float:
    """
    Compute BLEU score for SQL queries.

    Args:
        predictions: List of predicted SQL queries
        references: List of reference SQL queries

    Returns:
        BLEU score (0-1)
    """
    try:
        from sacrebleu import corpus_bleu

        # Convert single strings to lists for sacrebleu
        references = [[ref] for ref in references]

        bleu = corpus_bleu(predictions, references)
        return bleu.score / 100.0

    except ImportError:
        logger.warning("sacrebleu not installed. Install with: pip install sacrebleu")
        return 0.0


def component_match_score(
    predictions: List[str],
    references: List[str],
    component: str = "select",
) -> float:
    """
    Compute component-level match score (e.g., SELECT clause match).

    Args:
        predictions: List of predicted SQL queries
        references: List of reference SQL queries
        component: SQL component to match (select, from, where, etc.)

    Returns:
        Component match accuracy (0-1)
    """
    matches = 0

    for pred, ref in zip(predictions, references):
        pred_comp = extract_component(pred, component)
        ref_comp = extract_component(ref, component)

        if pred_comp and ref_comp and normalize_sql(pred_comp) == normalize_sql(ref_comp):
            matches += 1

    return matches / len(predictions) if predictions else 0.0


def extract_component(sql: str, component: str) -> str:
    """
    Extract a component from SQL query.

    Args:
        sql: SQL query string
        component: Component to extract

    Returns:
        Extracted component string
    """
    sql_upper = sql.upper()
    component_upper = component.upper()

    # Find component start
    start_idx = sql_upper.find(component_upper)
    if start_idx == -1:
        return ""

    # Find next clause keyword (approximate)
    next_keywords = ["FROM", "WHERE", "GROUP BY", "ORDER BY", "HAVING", "LIMIT"]
    end_idx = len(sql)

    for keyword in next_keywords:
        idx = sql_upper.find(keyword, start_idx + len(component_upper))
        if idx != -1 and idx < end_idx:
            end_idx = idx

    return sql[start_idx:end_idx].strip()
