# Text2SQL Documentation

Welcome to the Text2SQL documentation! This comprehensive guide will help you get started with fine-tuning Large Language Models for SQL generation.

## Quick Links

- [Installation Guide](installation.md)
- [Quick Start Tutorial](quickstart.md)
- [Training Guide](training.md)
- [Evaluation Guide](evaluation.md)
- [API Reference](api_reference.md)
- [Deployment Guide](deployment.md)
- [Architecture Overview](architecture.md)

## What is Text2SQL?

Text2SQL is a production-grade framework for fine-tuning Large Language Models to convert natural language questions into SQL queries. It provides:

- **Multi-Model Support**: CodeLlama, Mistral, Phi-2, and more
- **Efficient Training**: LoRA and QLoRA for parameter-efficient fine-tuning
- **Production-Ready**: Complete with REST API, Docker support, and testing
- **Comprehensive Evaluation**: Multiple metrics and benchmark datasets

## Getting Started

1. **Installation**: Follow the [installation guide](installation.md)
2. **Quick Start**: Try the [quick start tutorial](quickstart.md)
3. **Training**: Learn how to [train your own model](training.md)
4. **Deployment**: Deploy your model with the [deployment guide](deployment.md)

## Features

### Training Methods

- **Full Fine-Tuning**: Traditional fine-tuning of all model parameters
- **LoRA**: Low-Rank Adaptation for efficient fine-tuning
- **QLoRA**: Quantized LoRA for memory-efficient training

### Supported Datasets

- Spider (10,181 examples)
- WikiSQL (80,654 examples)
- BIRD (12,751 examples)
- CoSQL (3,007 dialogues)
- Custom datasets

### Model Architecture

The framework supports various base models:
- CodeLlama (7B, 13B)
- Mistral (7B)
- DeepSeek-Coder (6.7B)
- Phi-2 (2.7B)
- Llama-2 (7B, 13B)

## Community

- [GitHub Repository](https://github.com/yourusername/LLM-Finetuning)
- [Issue Tracker](https://github.com/yourusername/LLM-Finetuning/issues)
- [Contributing Guide](../CONTRIBUTING.md)

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
