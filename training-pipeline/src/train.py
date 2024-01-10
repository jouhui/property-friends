import joblib
import numpy as np
import pandas as pd
from category_encoders import TargetEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_error,
)
from sklearn.pipeline import Pipeline

from src import utils
from src.dataset import Dataloader


class Trainer:
    def __init__(self, dataloader: Dataloader) -> None:
        self.dataloader = dataloader
        self.train_set, self.test_set = dataloader.load_data()
        self.train_cols = [
            col for col in self.train_set.columns if col not in ["id", "target"]
        ]
        self.categorical_cols = ["type", "sector"]
        self.target_col = "price"
        self.pipeline = self._build_pipeline()

    def _build_pipeline(self) -> Pipeline:
        preprocessor = self._get_preprocessor()
        model = GradientBoostingRegressor(
            **{
                "learning_rate": 0.01,
                "n_estimators": 300,
                "max_depth": 5,
                "loss": "absolute_error",
            }
        )
        steps = [
            ("preprocessor", preprocessor),
            ("model", model),
        ]
        return Pipeline(steps)

    def _get_preprocessor(self) -> ColumnTransformer:
        categorical_transformer = TargetEncoder()
        preprocessor = ColumnTransformer(
            transformers=[
                ("categorical", categorical_transformer, self.categorical_cols)
            ]
        )
        return preprocessor

    def train(self, model_filename: str, upload_to_gcs: bool = False) -> None:
        self.pipeline.fit(
            self.train_set[self.train_cols], self.train_set[self.target_col]
        )
        self._save_model(model_filename, upload_to_gcs)

    def _save_model(self, model_filename: str, upload_to_gcs: bool = False) -> None:
        joblib.dump(self.pipeline, model_filename)

        if upload_to_gcs:
            utils.upload_to_gcs(model_filename)

    def evaluate(self, test_set: pd.DataFrame | None = None) -> None:
        if test_set is None:
            test_set = self.test_set

        predictions = self.pipeline.predict(test_set[self.train_cols])
        target = test_set[self.target_col].values

        print("RMSE: ", np.sqrt(mean_squared_error(predictions, target)))
        print("MAPE: ", mean_absolute_percentage_error(predictions, target))
        print("MAE : ", mean_absolute_error(predictions, target))


if __name__ == "__main__":
    from src.dataset import CsvDataloader

    dataloader = CsvDataloader(train_path="data/train.csv", test_path="data/test.csv")
    trainer = Trainer(dataloader)
    trainer.train(model_filename="models/model.joblib", upload_to_gcs=True)
    trainer.evaluate()
