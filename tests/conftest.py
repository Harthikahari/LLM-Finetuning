"""Pytest configuration and fixtures."""

import pytest
from text2sql.data.datasets import Text2SQLExample


@pytest.fixture
def sample_example():
    """Sample Text2SQL example."""
    return Text2SQLExample(
        question="What are all employee names?",
        query="SELECT name FROM employees;",
        db_id="company",
        tables=["employees"],
        columns={"employees": ["id", "name", "department"]},
    )


@pytest.fixture
def sample_examples():
    """List of sample examples."""
    return [
        Text2SQLExample(
            question="What are all employee names?",
            query="SELECT name FROM employees;",
            db_id="company",
        ),
        Text2SQLExample(
            question="Count all employees",
            query="SELECT COUNT(*) FROM employees;",
            db_id="company",
        ),
    ]
