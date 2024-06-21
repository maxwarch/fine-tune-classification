from transformers import CamembertTokenizer, CamembertForSequenceClassification

checkpoint = "almanach/camembert-base"
tokenizer = CamembertTokenizer.from_pretrained(checkpoint)
model = CamembertForSequenceClassification.from_pretrained(checkpoint)


t = tokenizer(
    "Ceci est un texte à tokenizer",
    padding="max_length",
    max_length=11,
    truncation=True,
)

print(tokenizer.convert_ids_to_tokens(t["input_ids"]))
