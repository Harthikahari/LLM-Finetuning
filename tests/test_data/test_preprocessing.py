"""Tests for data preprocessing."""

import pytest
from text2sql.data.preprocessing import clean_query, normalize_sql, is_valid_example


def test_clean_query():
    """Test SQL query cleaning."""
    query = "  SELECT   name  FROM   employees  "
    cleaned = clean_query(query)
    assert "SELECT" in cleaned
    assert "  " not in cleaned


def test_normalize_sql():
    """Test SQL normalization."""
    sql1 = "SELECT name FROM employees"
    sql2 = "select name from employees;"
    assert normalize_sql(sql1) == normalize_sql(sql2)


def test_is_valid_example(sample_example):
    """Test example validation."""
    assert is_valid_example(sample_example) is True
