import pandas as pd
from category_encoders import TargetEncoder
from sklearn.compose import ColumnTransformer

from src.dataloader import Dataloader


class DataProcessor:
    """Processor class that receives the data given by a dataloader and prepares it for training"""

    def __init__(self, dataloader: Dataloader) -> None:
        self.train_set = dataloader.load_train_data()
        self.test_set = dataloader.load_test_data()
        self.train_cols = [col for col in self.train_set.columns if col not in ["id", "target"]]
        self.categorical_cols = ["type", "sector"]
        self.target_col = "price"

    def get_train_data(self) -> tuple[pd.DataFrame, pd.Series]:
        return self.train_set[self.train_cols], self.train_set[self.target_col]

    def get_test_data(self) -> tuple[pd.DataFrame, pd.Series]:
        return self.test_set[self.train_cols], self.test_set[self.target_col]

    def get_train_cols(self) -> list[str]:
        return self.train_cols

    def get_target_col(self) -> str:
        return self.target_col

    def get_preprocessor(self) -> ColumnTransformer:
        categorical_transformer = TargetEncoder()
        preprocessor = ColumnTransformer(
            transformers=[("categorical", categorical_transformer, self.categorical_cols)]
        )
        return preprocessor
