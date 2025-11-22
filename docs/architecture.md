# Architecture Overview

System architecture and design decisions.

## High-Level Architecture

```
┌─────────────────┐
│   User Input    │
│  (NL Question)  │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Data Pipeline  │
│  - Loading      │
│  - Preprocessing│
│  - Augmentation │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Model Layer    │
│  - Base Models  │
│  - LoRA/QLoRA   │
└────────┬────────┘
         │
         v
┌─────────────────┐
│    Training     │
│  - Trainer      │
│  - Callbacks    │
│  - Metrics      │
└────────┬────────┘
         │
         v
┌─────────────────┐
│   Evaluation    │
│  - Benchmarks   │
│  - SQL Executor │
└────────┬────────┘
         │
         v
┌─────────────────┐
│   Inference     │
│  - Predictor    │
│  - Optimization │
└────────┬────────┘
         │
         v
┌─────────────────┐
│   REST API      │
│   (FastAPI)     │
└─────────────────┘
```

## Component Design

### Data Pipeline
- Dataset loaders for multiple sources
- Preprocessing with SQL normalization
- Data augmentation for robustness

### Model Layer
- Factory pattern for model creation
- Support for multiple architectures
- Efficient parameter-efficient methods

### Training
- Custom trainer extending HuggingFace
- SQL-specific callbacks
- Comprehensive metrics

### Evaluation
- Multiple evaluation metrics
- SQL execution validation
- Benchmark support

### Inference
- Optimized prediction pipeline
- Batch processing support
- Model quantization

### API
- FastAPI for high performance
- OpenAPI documentation
- Docker deployment
