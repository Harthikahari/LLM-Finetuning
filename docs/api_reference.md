# API Reference

Complete API reference for Text2SQL.

## REST API

### POST /predict

Generate SQL from natural language.

**Request:**
```json
{
    "question": "What are all employee names?",
    "schema": "employees(id, name, department)",
    "max_new_tokens": 256,
    "temperature": 0.1
}
```

**Response:**
```json
{
    "queries": ["SELECT name FROM employees;"],
    "question": "What are all employee names?"
}
```

### POST /predict/batch

Batch prediction endpoint.

**Request:**
```json
{
    "questions": ["Query 1", "Query 2"],
    "schemas": ["schema1", "schema2"]
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
    "status": "healthy",
    "model_loaded": true,
    "version": "0.1.0"
}
```

### GET /model/info

Get model information.

**Response:**
```json
{
    "model_name": "codellama-7b",
    "model_type": "text2sql",
    "parameters": 7000000000,
    "device": "cuda"
}
```

## Python API

### Model Factory

```python
from text2sql.models.model_factory import create_model

model = create_model(
    model_name="codellama-7b",
    training_method="qlora",
    lora_r=16,
    lora_alpha=32
)
```

### Predictor

```python
from text2sql.inference.predictor import Text2SQLPredictor

predictor = Text2SQLPredictor(model, tokenizer)
queries = predictor.predict("What are all employee names?")
```

### Evaluator

```python
from text2sql.evaluation.evaluator import evaluate_model

results = evaluate_model(model, tokenizer, eval_dataset)
```
