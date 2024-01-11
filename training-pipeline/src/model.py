from typing import Protocol

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline

from src.data_processing import DataProcessor


class Model(Protocol):
    def train(self, X_train: pd.DataFrame, y_train: pd.DataFrame) -> None:
        ...

    def predict(self, X_test: pd.DataFrame) -> np.ndarray:
        ...

    def save_model(self, model_path: str) -> None:
        ...


class GradientBoostingRegressorModel:
    def __init__(self, data_processor: DataProcessor, random_seed: int = 0) -> None:
        model = GradientBoostingRegressor(
            **{
                "learning_rate": 0.01,
                "n_estimators": 300,
                "max_depth": 5,
                "loss": "absolute_error",
                "random_state": random_seed,
            }
        )

        preprocessor = data_processor.get_preprocessor()
        steps = [
            ("preprocessor", preprocessor),
            ("model", model),
        ]
        self.pipeline = Pipeline(steps)

    def train(self, X_train: pd.DataFrame, y_train: pd.DataFrame) -> None:
        self.pipeline.fit(X_train, y_train)

    def predict(self, X_test: pd.DataFrame) -> np.ndarray:
        return self.pipeline.predict(X_test)

    def save_model(self, model_filename: str) -> None:
        joblib.dump(self.pipeline, model_filename)
