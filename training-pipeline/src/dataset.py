from typing import Protocol

import pandas as pd


class Dataloader(Protocol):
    def load_data(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        ...


class CsvDataloader:
    def __init__(self, train_path: str, test_path: str):
        self.train_path = train_path
        self.test_path = test_path

    def load_data(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        train = pd.read_csv(self.train_path)
        test = pd.read_csv(self.test_path)
        return train, test
