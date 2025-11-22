"""Pydantic schemas for API requests and responses."""

from pydantic import BaseModel, Field
from typing import List, Optional


class PredictionRequest(BaseModel):
    """Request schema for single prediction."""

    question: str = Field(..., description="Natural language question")
    schema: Optional[str] = Field(None, description="Database schema")
    max_new_tokens: int = Field(256, description="Maximum tokens to generate")
    temperature: float = Field(0.1, description="Sampling temperature")
    num_return_sequences: int = Field(1, description="Number of queries to generate")

    class Config:
        schema_extra = {
            "example": {
                "question": "What are the names of all employees?",
                "schema": "employees(id, name, department)",
                "max_new_tokens": 256,
                "temperature": 0.1,
                "num_return_sequences": 1,
            }
        }


class PredictionResponse(BaseModel):
    """Response schema for prediction."""

    queries: List[str] = Field(..., description="Generated SQL queries")
    question: str = Field(..., description="Original question")

    class Config:
        schema_extra = {
            "example": {
                "queries": ["SELECT name FROM employees;"],
                "question": "What are the names of all employees?",
            }
        }


class BatchPredictionRequest(BaseModel):
    """Request schema for batch prediction."""

    questions: List[str] = Field(..., description="List of questions")
    schemas: Optional[List[str]] = Field(None, description="List of schemas")
    max_new_tokens: int = Field(256, description="Maximum tokens to generate")
    temperature: float = Field(0.1, description="Sampling temperature")


class BatchPredictionResponse(BaseModel):
    """Response schema for batch prediction."""

    queries: List[str] = Field(..., description="Generated SQL queries")
    count: int = Field(..., description="Number of predictions")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    model_loaded: bool
    version: str


class ModelInfo(BaseModel):
    """Model information response."""

    model_name: str
    model_type: str
    parameters: int
    device: str
