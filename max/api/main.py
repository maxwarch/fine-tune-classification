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


text = """Après de multiples tournées à succès et plus de 2 millions de billets vendus, Messmer, connu et reconnu comme le Maître Mondial de l’Hypnose revient près de chez vous !

Dans 13Hz, Messmer vous invite à entrer dans son mystérieux et hilarant univers où la frontière entre la réalité et l’illusion s’efface, pour diriger vos pensées vers des territoires inconnus.

Avec sa présence charismatique inégalée et son talent exceptionnel, le recordman en hypnose collective avec 1066 personnes hypnotisées en moins de 5 minutes, vous plonge au cœur de vos pensées les plus profondes avant de vous guider à travers un jeu subtil d’ondes cérébrales à 13Hz.

Le fascinateur vous entraîne vers un état de conscience unique où la volonté et le contrôle de nos vies prennent une nouvelle dimension.

Osez découvrir l’expérience Messmer, où la maîtrise de soi et la fascination se rencontrent."""


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


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
