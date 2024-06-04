from transformers import AutoTokenizer
from datasets import Dataset
import torch
import pandas as pd
from labels import LABELS


class EventDataset:
    def __init__(self, data_path: str, do_clean=True) -> None:
        self.df = pd.read_csv(data_path)
        if do_clean:
            self.ohe_clean()

    def __len__(self):
        return self.df.shape

    def __call__(self) -> pd.DataFrame:
        return self.df

    def ohe_clean(self):
        self.df.dropna(subset=["description"], inplace=True)

        for label in LABELS:
            self.df.insert(
                self.df.shape[1],
                label,
                pd.Series(0, dtype=int, index=range(self.df.shape[0])),
            )

        for row in self.df.iterrows():
            for cat in ["cat1", "cat2", "cat3"]:
                for cat_col in LABELS:
                    if row[1].loc[cat] == cat_col:
                        self.df.at[row[0], cat_col] = 1
                        break

        self.df.description = self.df.description.replace(
            to_replace=r"\n+|\s+", value=" ", regex=True
        )
        self.df.drop(columns=["cat1", "cat2", "cat3", "url"], inplace=True)
        self.df = self.df.iloc[:, 1:]

        return self.df

    def add_column(self, name: str):
        self.df[name] = pd.Series().fillna("")


class EventTokenizeDataset(Dataset):
    def __init__(self, data: pd.DataFrame, tokenizer=None, max_token_len: int = 128):
        self.df = data
        self.tokenizer = (
            tokenizer
            if tokenizer is not None
            else AutoTokenizer.from_pretrained("camembert-base")
        )
        self.max_token_len = max_token_len

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index: int):
        data_row = self.df.iloc[index]

        description_text = (
            data_row.resume
            if isinstance(data_row.resume, str)
            else data_row.description
        )

        # description_text = data_row.description
        labels = data_row[LABELS]

        self.encoding = self.tokenizer.encode_plus(
            description_text,
            add_special_tokens=True,
            max_length=self.max_token_len,
            return_token_type_ids=False,
            padding="max_length",
            truncation=True,
            return_attention_mask=True,
            return_tensors="pt",
        )

        return dict(
            description_text=description_text.strip().replace("\n", " "),
            input_ids=self.encoding["input_ids"].flatten(),
            attention_mask=self.encoding["attention_mask"].flatten(),
            labels=torch.FloatTensor(labels),
        )

    def tokenized_str(self, input_id):
        return self.tokenizer.convert_ids_to_tokens(input_id.squeeze())
