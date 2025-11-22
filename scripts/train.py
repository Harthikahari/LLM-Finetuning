#!/usr/bin/env python3
"""
Training script for Text2SQL fine-tuning.

Example usage:
    python scripts/train.py --model codellama-7b --dataset spider --method qlora
"""

import argparse
import logging
from pathlib import Path

from text2sql.utils.logging import setup_logging
from text2sql.utils.config import load_config
from text2sql.utils.helpers import set_seed
from text2sql.data.datasets import load_dataset, Text2SQLDataset
from text2sql.models.model_factory import create_model
from text2sql.training.trainer import create_trainer


def parse_args():
    parser = argparse.ArgumentParser(description="Train Text2SQL model")

    parser.add_argument("--model", type=str, required=True, help="Model name")
    parser.add_argument("--dataset", type=str, required=True, help="Dataset name")
    parser.add_argument("--method", type=str, default="qlora", choices=["full", "lora", "qlora"])
    parser.add_argument("--output_dir", type=str, default="./outputs")
    parser.add_argument("--config", type=str, help="Path to config file")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--learning_rate", type=float, default=2e-4)

    return parser.parse_args()


def main():
    args = parse_args()

    # Setup logging
    setup_logging(level="INFO", log_file=f"{args.output_dir}/training.log")
    logger = logging.getLogger(__name__)

    logger.info("Starting Text2SQL training")
    logger.info(f"Arguments: {args}")

    # Set seed
    set_seed(args.seed)

    # Load config if provided
    config = {}
    if args.config:
        config = load_config(args.config)
        logger.info(f"Loaded config from {args.config}")

    # Load dataset
    logger.info(f"Loading dataset: {args.dataset}")
    train_examples = load_dataset(args.dataset, split="train")
    eval_examples = load_dataset(args.dataset, split="validation")

    logger.info(f"Loaded {len(train_examples)} train examples, {len(eval_examples)} eval examples")

    # Create model
    logger.info(f"Creating model: {args.model} with method: {args.method}")
    model = create_model(
        model_name=args.model,
        training_method=args.method,
        **config.get("model", {})
    )

    # Create datasets
    train_dataset = Text2SQLDataset(
        examples=train_examples,
        tokenizer=model.tokenizer,
        max_length=config.get("max_length", 512),
    )

    eval_dataset = Text2SQLDataset(
        examples=eval_examples,
        tokenizer=model.tokenizer,
        max_length=config.get("max_length", 512),
    )

    # Create trainer
    trainer = create_trainer(
        model=model.model,
        tokenizer=model.tokenizer,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        output_dir=args.output_dir,
        num_train_epochs=args.num_epochs,
        per_device_train_batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        **config.get("training", {})
    )

    # Train
    logger.info("Starting training")
    trainer.train()

    # Save model
    logger.info(f"Saving model to {args.output_dir}")
    model.save_pretrained(args.output_dir)

    logger.info("Training completed")


if __name__ == "__main__":
    main()
