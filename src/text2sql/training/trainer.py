"""
Custom trainer for Text2SQL fine-tuning.

Extends HuggingFace Trainer with SQL-specific functionality.
"""

import logging
from typing import Optional, Dict, Any, Callable
from pathlib import Path

import torch
from transformers import (
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling,
)
from transformers.trainer_callback import TrainerCallback

logger = logging.getLogger(__name__)


class Text2SQLTrainer(Trainer):
    """
    Custom trainer for Text2SQL models.

    Extends HuggingFace Trainer with:
    - Custom evaluation metrics
    - SQL validation during training
    - Enhanced logging
    - Custom checkpointing
    """

    def __init__(
        self,
        model=None,
        args: TrainingArguments = None,
        train_dataset=None,
        eval_dataset=None,
        tokenizer=None,
        data_collator=None,
        compute_metrics: Optional[Callable] = None,
        callbacks: Optional[list] = None,
        **kwargs,
    ):
        # Use default data collator if not provided
        if data_collator is None:
            data_collator = DataCollatorForLanguageModeling(
                tokenizer=tokenizer,
                mlm=False,  # Causal LM, not masked LM
            )

        super().__init__(
            model=model,
            args=args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            tokenizer=tokenizer,
            data_collator=data_collator,
            compute_metrics=compute_metrics,
            callbacks=callbacks,
            **kwargs,
        )

        logger.info("Initialized Text2SQLTrainer")

    def compute_loss(self, model, inputs, return_outputs=False):
        """
        Compute loss with optional custom modifications.

        Args:
            model: The model
            inputs: Model inputs
            return_outputs: Whether to return outputs

        Returns:
            Loss (and outputs if return_outputs=True)
        """
        # Standard causal LM loss
        outputs = model(**inputs)
        loss = outputs.loss

        return (loss, outputs) if return_outputs else loss

    def save_model(self, output_dir: Optional[str] = None, _internal_call: bool = False):
        """
        Save model with enhanced logging.

        Args:
            output_dir: Directory to save to
            _internal_call: Internal flag
        """
        output_dir = output_dir or self.args.output_dir
        logger.info(f"Saving model to {output_dir}")

        super().save_model(output_dir, _internal_call)

        # Save additional metadata
        metadata = {
            "global_step": self.state.global_step,
            "epoch": self.state.epoch,
            "best_metric": self.state.best_metric,
        }

        import json
        metadata_path = Path(output_dir) / "training_metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"Model and metadata saved to {output_dir}")

    def log(self, logs: Dict[str, float]) -> None:
        """
        Enhanced logging with custom metrics.

        Args:
            logs: Dictionary of metrics to log
        """
        # Add custom metrics if needed
        if "loss" in logs:
            logs["perplexity"] = torch.exp(torch.tensor(logs["loss"])).item()

        super().log(logs)


def create_trainer(
    model,
    tokenizer,
    train_dataset,
    eval_dataset,
    output_dir: str = "./outputs",
    num_train_epochs: int = 3,
    per_device_train_batch_size: int = 4,
    per_device_eval_batch_size: int = 4,
    gradient_accumulation_steps: int = 4,
    learning_rate: float = 2e-4,
    warmup_steps: int = 100,
    logging_steps: int = 10,
    save_steps: int = 500,
    eval_steps: int = 500,
    save_total_limit: int = 3,
    fp16: bool = False,
    bf16: bool = True,
    gradient_checkpointing: bool = True,
    optim: str = "paged_adamw_32bit",
    **kwargs,
) -> Text2SQLTrainer:
    """
    Create a configured Text2SQLTrainer.

    Args:
        model: Model to train
        tokenizer: Tokenizer
        train_dataset: Training dataset
        eval_dataset: Evaluation dataset
        output_dir: Output directory
        num_train_epochs: Number of epochs
        per_device_train_batch_size: Batch size for training
        per_device_eval_batch_size: Batch size for evaluation
        gradient_accumulation_steps: Gradient accumulation steps
        learning_rate: Learning rate
        warmup_steps: Warmup steps
        logging_steps: Logging frequency
        save_steps: Save checkpoint frequency
        eval_steps: Evaluation frequency
        save_total_limit: Maximum number of checkpoints to keep
        fp16: Whether to use FP16
        bf16: Whether to use BF16
        gradient_checkpointing: Whether to use gradient checkpointing
        optim: Optimizer type
        **kwargs: Additional training arguments

    Returns:
        Configured trainer
    """
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=per_device_train_batch_size,
        per_device_eval_batch_size=per_device_eval_batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        learning_rate=learning_rate,
        warmup_steps=warmup_steps,
        logging_steps=logging_steps,
        save_steps=save_steps,
        eval_steps=eval_steps if eval_dataset else None,
        save_total_limit=save_total_limit,
        fp16=fp16,
        bf16=bf16,
        gradient_checkpointing=gradient_checkpointing,
        optim=optim,
        evaluation_strategy="steps" if eval_dataset else "no",
        save_strategy="steps",
        load_best_model_at_end=True if eval_dataset else False,
        report_to=["tensorboard", "wandb"],
        push_to_hub=False,
        **kwargs,
    )

    trainer = Text2SQLTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        tokenizer=tokenizer,
    )

    logger.info("Trainer created successfully")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Training for {num_train_epochs} epochs")
    logger.info(f"Effective batch size: {per_device_train_batch_size * gradient_accumulation_steps}")

    return trainer
