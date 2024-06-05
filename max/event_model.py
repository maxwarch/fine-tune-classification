import lightning as L
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
    def __init__(self, n_classes: int, n_training_steps=None, n_warmup_steps=None):
        super().__init__()
        self.model = CamembertForSequenceClassification.from_pretrained(
            "camembert-base", problem_type="multi_label_classification"
        )
        self.classifier = nn.Linear(self.model.config.hidden_size, n_classes)
        self.n_training_steps = n_training_steps
        self.n_warmup_steps = n_warmup_steps
        self.criterion = nn.BCELoss()
        self.num_labels = n_classes

    def forward(self, batch):
        output = self.model(
            input_ids=batch["input_ids"], attention_mask=batch["attention_mask"]
        )
        return output

    def training_step(self, batch, batch_idx):
        out = self.forward(batch)
        logits = out.logits
        # -------- MASKED --------
        loss_fn = torch.nn.CrossEntropyLoss()
        loss = loss_fn(logits.view(-1, self.num_labels), batch["labels"].view(-1))

        # ------ END MASKED ------

        self.log("train/loss", loss)

        return loss

    def validation_step(self, batch, batch_idx):
        out = self.forward(batch)
        logits = out.logits
        # -------- MASKED --------
        loss_fn = torch.nn.CrossEntropyLoss()
        loss = loss_fn(logits.view(-1, self.num_labels), batch["labels"].view(-1))

        # ------ END MASKED ------

        self.log("train/loss", loss)

        return loss

    def predict_step(self, batch, batch_idx):
        """La fonction predict step facilite la prédiction de données. Elle est
        similaire à `validation_step`, sans le calcul des métriques.
        """
        out = self.forward(batch)

        return torch.max(out.logits, -1).indices

    def on_train_epoch_end(self, outputs):
        labels = []
        predictions = []
        for output in outputs:
            for out_labels in output["labels"].detach().cpu():
                labels.append(out_labels)
            for out_predictions in output["predictions"].detach().cpu():
                predictions.append(out_predictions)
        labels = torch.stack(labels).int()
        predictions = torch.stack(predictions)
        for i, name in enumerate(LABELS):
            ml_auroc = multilabel_auroc(
                predictions[:, i], labels[:, i], num_labels=len(LABELS), average="macro"
            )
            self.logger.experiment.add_scalar(
                f"{name}_roc_auc/Train", ml_auroc, self.current_epoch
            )

    def configure_optimizers(self):
        optimizer = AdamW(self.parameters(), lr=2e-5)
        # scheduler = get_linear_schedule_with_warmup(
        #     optimizer,
        #     # num_warmup_steps=self.n_warmup_steps,
        #     # num_training_steps=self.n_training_steps,
        # )
        return dict(
            optimizer=optimizer  # , lr_scheduler=dict(scheduler=scheduler, interval="step")
        )
