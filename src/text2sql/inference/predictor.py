"""Predictor for Text2SQL inference."""

import logging
from typing import List, Dict, Optional
import torch

logger = logging.getLogger(__name__)


class Text2SQLPredictor:
    """Predictor for Text2SQL inference."""

    def __init__(
        self,
        model,
        tokenizer,
        max_new_tokens: int = 256,
        temperature: float = 0.1,
        device: Optional[str] = None,
    ):
        self.model = model
        self.tokenizer = tokenizer
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        self.model.to(self.device)
        self.model.eval()

    def predict(
        self,
        question: str,
        schema: Optional[str] = None,
        num_return_sequences: int = 1,
    ) -> List[str]:
        """Predict SQL query from question."""
        # Format prompt
        if schema:
            prompt = f"Schema: {schema}\nQuestion: {question}\nSQL:"
        else:
            prompt = f"Question: {question}\nSQL:"

        # Generate
        queries = self.model.generate(
            prompt,
            max_new_tokens=self.max_new_tokens,
            temperature=self.temperature,
            num_return_sequences=num_return_sequences,
        )

        return queries

    def batch_predict(
        self,
        questions: List[str],
        schemas: Optional[List[str]] = None,
        batch_size: int = 4,
    ) -> List[str]:
        """Batch prediction."""
        results = []

        for i in range(0, len(questions), batch_size):
            batch_questions = questions[i:i+batch_size]
            batch_schemas = schemas[i:i+batch_size] if schemas else [None] * len(batch_questions)

            for question, schema in zip(batch_questions, batch_schemas):
                predictions = self.predict(question, schema)
                results.append(predictions[0])

        return results
