# Training Guide

Comprehensive guide to training Text2SQL models.

## Quick Start

```bash
python scripts/train.py --model codellama-7b --dataset spider --method qlora
```

## Training Methods

### QLoRA (Recommended)

Memory-efficient training with 4-bit quantization:

```bash
python scripts/train.py \
    --model codellama-7b \
    --dataset spider \
    --method qlora \
    --batch_size 4 \
    --num_epochs 3
```

### LoRA

Efficient training without quantization:

```bash
python scripts/train.py \
    --model mistral-7b-instruct \
    --dataset spider \
    --method lora \
    --batch_size 2 \
    --num_epochs 3
```

### Full Fine-Tuning

Train all model parameters:

```bash
python scripts/train.py \
    --model phi-2 \
    --dataset wikisql \
    --method full \
    --batch_size 1 \
    --num_epochs 3
```

## Advanced Configuration

Use YAML config files for complex setups:

```bash
python scripts/train.py --config configs/training/qlora_config.yaml
```

## Monitoring Training

Training logs are sent to:
- TensorBoard: `tensorboard --logdir outputs/runs`
- Weights & Biases: Automatic if logged in

## Hardware Requirements

| Model Size | Method | Min VRAM | Recommended |
|------------|--------|----------|-------------|
| 7B | QLoRA | 16GB | 24GB |
| 7B | LoRA | 24GB | 40GB |
| 13B | QLoRA | 24GB | 40GB |
| 13B | LoRA | 40GB | 80GB |
