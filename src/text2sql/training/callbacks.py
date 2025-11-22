"""Training callbacks for Text2SQL fine-tuning."""

import logging
from typing import Optional, List
from pathlib import Path

from transformers import TrainerCallback, TrainerState, TrainerControl, TrainingArguments

logger = logging.getLogger(__name__)


class SQLValidationCallback(TrainerCallback):
    """
    Callback to validate SQL queries during training.

    Generates sample predictions and validates them periodically.
    """

    def __init__(
        self,
        validation_examples: Optional[List] = None,
        validation_interval: int = 500,
    ):
        self.validation_examples = validation_examples or []
        self.validation_interval = validation_interval

    def on_step_end(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs,
    ):
        """Run validation at specified intervals."""
        if state.global_step % self.validation_interval == 0 and self.validation_examples:
            model = kwargs.get("model")
            tokenizer = kwargs.get("tokenizer")

            if model and tokenizer:
                logger.info(f"Running SQL validation at step {state.global_step}")
                self._validate_samples(model, tokenizer)

        return control

    def _validate_samples(self, model, tokenizer):
        """Validate sample predictions."""
        model.eval()

        for i, example in enumerate(self.validation_examples[:3]):  # Validate first 3
            try:
                question = example.question
                expected = example.query

                # Generate prediction
                inputs = tokenizer(question, return_tensors="pt").to(model.device)
                outputs = model.generate(**inputs, max_new_tokens=128)
                predicted = tokenizer.decode(outputs[0], skip_special_tokens=True)

                logger.info(f"Sample {i+1}:")
                logger.info(f"  Question: {question[:100]}")
                logger.info(f"  Expected: {expected[:100]}")
                logger.info(f"  Predicted: {predicted[:100]}")

            except Exception as e:
                logger.warning(f"Validation failed for sample {i+1}: {e}")

        model.train()


class CheckpointCallback(TrainerCallback):
    """
    Custom checkpoint management callback.

    Provides additional checkpoint handling beyond default behavior.
    """

    def __init__(
        self,
        save_optimizer: bool = True,
        save_metrics: bool = True,
    ):
        self.save_optimizer = save_optimizer
        self.save_metrics = save_metrics

    def on_save(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs,
    ):
        """Handle checkpoint saving."""
        checkpoint_dir = Path(args.output_dir) / f"checkpoint-{state.global_step}"

        if self.save_metrics and state.log_history:
            import json

            metrics_file = checkpoint_dir / "metrics.json"
            with open(metrics_file, "w") as f:
                json.dump(state.log_history, f, indent=2)

            logger.info(f"Saved metrics to {metrics_file}")

        return control


class WandbCallback(TrainerCallback):
    """
    Weights & Biases integration callback.

    Logs additional metrics and artifacts to W&B.
    """

    def __init__(self, project: str = "text2sql-finetuning", enabled: bool = True):
        self.project = project
        self.enabled = enabled
        self.wandb = None

        if self.enabled:
            try:
                import wandb
                self.wandb = wandb
            except ImportError:
                logger.warning("wandb not installed. Install with: pip install wandb")
                self.enabled = False

    def on_train_begin(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs,
    ):
        """Initialize W&B run."""
        if self.enabled and self.wandb:
            self.wandb.init(
                project=self.project,
                config=args.to_dict(),
            )
            logger.info(f"Initialized W&B project: {self.project}")

        return control

    def on_log(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        logs=None,
        **kwargs,
    ):
        """Log metrics to W&B."""
        if self.enabled and self.wandb and logs:
            self.wandb.log(logs, step=state.global_step)

        return control
