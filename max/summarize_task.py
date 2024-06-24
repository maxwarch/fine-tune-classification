import pandas as pd
from transformers import AutoTokenizer
from dataset import EventDataset
from max.summarization import summarize
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

do_summarize = False

MAX_TOKEN_LEN = 512
SOURCE_DATA = "../dataset.csv"
RESUME_DATA = "./dataset_resume.csv"

DATA_PATH = SOURCE_DATA if do_summarize else RESUME_DATA

dataobj = EventDataset(DATA_PATH, do_summarize)
data: pd.DataFrame = dataobj()


tokenizer = AutoTokenizer.from_pretrained("camembert-base")
to_summarize = []

for index, row in data.iterrows():
    to_tokenize = row["description"]

    if "resume" in data:
        to_tokenize = (
            row["resume"] if isinstance(row["resume"], str) else row["description"]
        )

    token_count = len(
        tokenizer.encode(to_tokenize, max_length=MAX_TOKEN_LEN, truncation=False)
    )
    if token_count > MAX_TOKEN_LEN:
        to_summarize.append((index, row.description, token_count))

print("Nombre de texte à résumer", len(to_summarize))

if do_summarize:
    # create column "resume" for description token > MAX_TOKEN_LEN
    dataobj.add_column("resume")

    text_to_send = to_summarize  # [-2:]
    resume = summarize([s[1] for s in text_to_send], 10)

    for index, item in enumerate(text_to_send):
        data.loc[item[0], "resume"] = resume[index]

    data.to_csv(RESUME_DATA)
