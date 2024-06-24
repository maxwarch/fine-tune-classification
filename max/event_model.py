from pathlib import Path
from typing import Optional, Union, Tuple
import lightning as L
from lightning.pytorch.utilities.types import OptimizerLRScheduler
from torchmetrics.functional import accuracy
import torch.nn as nn
import torch
from torchmetrics.functional.classification import multilabel_auroc
from transformers import (
    CamembertForSequenceClassification,
    AdamW,
    # get_linear_schedule_with_warmup,
)

from labels import LABELS


class EventClassifier(L.LightningModule):
    def __init__(self, n_classes: int):
        super().__init__()

        self.model = CamembertForSequenceClassification.from_pretrained(
            "camembert-base", problem_type="multi_label_classification"
        )

        self.input_key = "input_ids"
        self.label_key = "labels"
        self.mask_key = "attention_mask"
        self.output_key = "logits"
        self.loss_key = "loss"
        self.accuracy = accuracy
        self.learning_rate = 5e-05
        self.num_labels = n_classes

    def forward(self, batch) -> torch.Any:
        print(batch[self.label_key])
        print(batch[self.input_key])
        output = self.model(
            batch[self.input_key],
            attention_mask=batch[self.mask_key],
            labels=batch[self.label_key],
        )
        print("***")
        print(output)
        return output

    def training_step(self, batch, batch_idx) -> torch.Tensor:
        output = self(batch)
        self.log("train-loss", output[self.loss_key])

        return output[self.loss_key]

    def validation_step(self, batch, batch_idx) -> None:
        """
        Notes:
            https://lightning.ai/docs/pytorch/stable/common/lightning_module.html#validation
        """
        output = self(batch)
        self.log("val-loss", output[self.loss_key], prog_bar=True)

        logits = output[self.output_key]
        predicted_labels = torch.argmax(logits, 1)
        acc = self.accuracy(
            predicted_labels,
            batch[self.label_key],
            num_classes=self.num_classes,
            task="multilabel",
        )
        self.log("val-acc", acc, prog_bar=True)

    def test_step(self, batch, batch_idx) -> None:
        """
        Notes:
            https://lightning.ai/docs/pytorch/stable/common/lightning_module.html#testing
        """
        output = self(batch)

        logits = output[self.output_key]
        predicted_labels = torch.argmax(logits, 1)
        acc = self.accuracy(
            predicted_labels,
            batch[self.label_key],
            num_classes=self.num_classes,
            task="multiclass",
        )
        self.log("test-acc", acc, prog_bar=True)

    # def predict_step(
    #     self, sequence: str, cache_dir: Union[str, Path] = Config.cache_dir
    # ) -> str:
    #     """
    #     Notes:
    #         https://lightning.ai/docs/pytorch/stable/common/lightning_module.html#inference
    #     """
    #     batch = tokenize_text(sequence, model_name=self.model_name, cache_dir=cache_dir)
    #     # autotokenizer may cause tokens to lose device type and cause failure
    #     batch = batch.to(self.device)
    #     outputs = self.model(batch[self.input_key])
    #     logits = outputs[self.output_key]
    #     predicted_label_id = torch.argmax(logits)
    #     labels = {0: "negative", 1: "positive"}
    #     return labels[predicted_label_id.item()]

    def configure_optimizers(self) -> OptimizerLRScheduler:
        optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate)
        return optimizer
