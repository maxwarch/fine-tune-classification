from fastapi import FastAPI
from transformers import logging as TFLogging
from transformers import (
    CamembertForSequenceClassification,
    CamembertTokenizerFast,
    Trainer,
    pipeline,
)

TFLogging.set_verbosity_error()

checkpoint = "almanach/camembert-base"
path = "./camembert-tourism-events"
tokenizer = CamembertTokenizerFast.from_pretrained(checkpoint)
model = CamembertForSequenceClassification.from_pretrained(path)
trainer = Trainer(model=model)


def sort_by_score(data):
    return sorted(data, key=lambda item: item["score"], reverse=True)


def predict_fn(text):
    predict = pipeline(
        task="text-classification",
        model=model,
        tokenizer=tokenizer,
        top_k=5,
    )
    return sort_by_score(predict(text)[0])


app = FastAPI()


@app.post("/predict")
def predict(text: str):
    return predict_fn(text)
