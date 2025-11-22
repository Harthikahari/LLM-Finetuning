# Quick Start Guide

Get up and running with Text2SQL in minutes!

## 1. Train Your First Model

```bash
# Train with QLoRA on Spider dataset
python scripts/train.py \
    --model codellama-7b \
    --dataset spider \
    --method qlora \
    --output_dir ./outputs \
    --num_epochs 1 \
    --batch_size 4
```

## 2. Run Inference

```bash
# Generate SQL from natural language
python scripts/inference.py \
    --model ./outputs \
    --question "What are the names of all employees?"
```

## 3. Start the API

```bash
# Start FastAPI server
uvicorn api.main:app --reload

# Test the API
curl -X POST "http://localhost:8000/predict" \
    -H "Content-Type: application/json" \
    -d '{
        "question": "Show me all products with price > 100",
        "schema": "products(id, name, price)"
    }'
```

## 4. Evaluate Your Model

```bash
# Evaluate on test set
python scripts/evaluate.py \
    --model ./outputs \
    --dataset spider \
    --split test
```

## Next Steps

- [Training Guide](training.md) - Learn advanced training techniques
- [API Reference](api_reference.md) - Explore the API
- [Deployment Guide](deployment.md) - Deploy to production
