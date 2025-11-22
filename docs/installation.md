# Installation Guide

This guide covers installing Text2SQL and its dependencies.

## Prerequisites

- Python 3.9 or higher
- CUDA 11.8+ (for GPU support)
- 24GB+ VRAM (for 7B models with QLoRA)

## Installation Methods

### From Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/LLM-Finetuning.git
cd LLM-Finetuning

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### Using Docker

```bash
# Build Docker image
docker-compose build

# Run container
docker-compose up training
```

## Verify Installation

```python
import text2sql
from text2sql.models.model_factory import ModelFactory

# List supported models
models = ModelFactory.list_supported_models()
print(models)
```

## GPU Setup

Verify CUDA is available:

```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
```

## Next Steps

- [Quick Start Tutorial](quickstart.md)
- [Training Guide](training.md)
