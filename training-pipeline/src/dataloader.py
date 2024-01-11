from typing import Protocol

import pandas as pd


class Dataloader(Protocol):
    def load_train_data(self) -> pd.DataFrame:
        ...

    def load_test_data(self) -> pd.DataFrame:
        ...


class CsvDataloader:
    """Dataloader that loads data from CSV files."""

    def __init__(self, train_path: str, test_path: str):
        self.train_path = train_path
        self.test_path = test_path

    def load_train_data(self) -> pd.DataFrame:
        train = pd.read_csv(self.train_path)
        return train

    def load_test_data(self) -> pd.DataFrame:
        test = pd.read_csv(self.test_path)
        return test


# To connect the pipeline with the database, just create another class that follows the Dataloader
# protocol, ensuring that the data loading methods return a pandas DataFrame with the same columns.
# That new class can be used in the trainer.Trainer method without any changes to the other classes.
