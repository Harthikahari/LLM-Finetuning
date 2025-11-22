"""Tests for dataset loading and processing."""

import pytest
from text2sql.data.datasets import Text2SQLExample, Text2SQLDataset


def test_text2sql_example(sample_example):
    """Test Text2SQLExample creation."""
    assert sample_example.question == "What are all employee names?"
    assert sample_example.query == "SELECT name FROM employees;"
    assert sample_example.db_id == "company"


def test_example_to_dict(sample_example):
    """Test example to dict conversion."""
    example_dict = sample_example.to_dict()
    assert "question" in example_dict
    assert "query" in example_dict
    assert "db_id" in example_dict


def test_text2sql_dataset(sample_examples):
    """Test Text2SQLDataset."""
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    dataset = Text2SQLDataset(
        examples=sample_examples,
        tokenizer=tokenizer,
        max_length=128,
    )

    assert len(dataset) == 2
    item = dataset[0]
    assert "input_ids" in item
    assert "attention_mask" in item
    assert "labels" in item
