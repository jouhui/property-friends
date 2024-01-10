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
from src.dataloader import Dataloader


class Trainer:
    """Trainer class that trains a model and evaluates it."""

    def __init__(self, dataloader: Dataloader, random_seed: int = 0) -> None:
        self.train_set = dataloader.load_train_data()
        self.test_set = dataloader.load_test_data()

        self.train_cols = [
            col for col in self.train_set.columns if col not in ["id", "target"]
        ]
        self.categorical_cols = ["type", "sector"]
        self.target_col = "price"

        self.pipeline = self._build_pipeline(random_seed)

    def _build_pipeline(self, random_seed: int = 0) -> Pipeline:
        """Build the pipeline for training."""
        preprocessor = self._get_preprocessor()
        model = GradientBoostingRegressor(
            **{
                "learning_rate": 0.01,
                "n_estimators": 300,
                "max_depth": 5,
                "loss": "absolute_error",
                "random_state": random_seed,
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
        """Train the model and save it.

        Args:
            model_filename (str):
                The filename in which the model will be saved.
            upload_to_gcs (bool, optional):
                Whether to upload the model to a GCS bucket. Defaults to False.
        """
        self.pipeline.fit(
            self.train_set[self.train_cols], self.train_set[self.target_col]
        )
        self._save_model(model_filename, upload_to_gcs)

    def _save_model(self, model_filename: str, upload_to_gcs: bool = False) -> None:
        """Save the model locally and optionally upload it to a GCS bucket.

        Args:
            model_filename (str):
                The filename in which the model will be saved.
            upload_to_gcs (bool, optional):
                Whether to upload the model to a GCS bucket. Defaults to False.
        """
        joblib.dump(self.pipeline, model_filename)

        if upload_to_gcs:
            utils.upload_to_gcs(model_filename)

    def evaluate(self, test_set: pd.DataFrame | None = None) -> None:
        """Evaluate the model on the test set and print the results.

        Args:
            test_set (pd.DataFrame | None, optional):
                The test set in which the model will be evaluated. If no test set is provided,
                the dataloader's default test set will be used. Defaults to None.

        Raises:
            ValueError: If the test set does not contain the same columns as the default test set.
        """
        if test_set is None:
            test_set = self.test_set
        else:
            if any(col in test_set.columns for col in self.test_set.cols):
                raise ValueError(
                    f"The test set must have all these columns: {self.test_set.cols}"
                )

        predictions = self.pipeline.predict(test_set[self.train_cols])
        target = test_set[self.target_col].values

        print("RMSE: ", np.sqrt(mean_squared_error(predictions, target)))
        print("MAPE: ", mean_absolute_percentage_error(predictions, target))
        print("MAE : ", mean_absolute_error(predictions, target))


if __name__ == "__main__":
    from src.dataloader import CsvDataloader

    dataloader = CsvDataloader(train_path="data/train.csv", test_path="data/test.csv")
    trainer = Trainer(dataloader)
    trainer.train(model_filename="models/model.joblib", upload_to_gcs=True)
    trainer.evaluate()
