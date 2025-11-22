# Evaluation Guide

Guide to evaluating Text2SQL models.

## Quick Evaluation

```bash
python scripts/evaluate.py --model ./outputs --dataset spider --split test
```

## Metrics

- **Exact Match**: Exact string match between predicted and reference SQL
- **Execution Accuracy**: Match based on query execution results
- **Component Match**: Match individual SQL components (SELECT, WHERE, etc.)

## Benchmark Evaluation

Run on standard benchmarks:

```bash
python scripts/benchmark.py --model ./outputs --benchmark spider
```

## Custom Evaluation

Use Python API for custom evaluation:

```python
from text2sql.models.model_factory import create_model
from text2sql.evaluation.evaluator import evaluate_model
from text2sql.data.datasets import load_dataset

model = create_model("./outputs", training_method="lora")
test_data = load_dataset("spider", split="test")

results = evaluate_model(model, model.tokenizer, test_data)
print(results)
```
