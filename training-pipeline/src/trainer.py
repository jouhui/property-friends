import numpy as np
import pandas as pd
import structlog
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_error,
)

from src import utils
from src.data_processing import DataProcessor
from src.dataloader import Dataloader
from src.model import Model

logger = structlog.get_logger()
logger.bind(module="trainer")


class Trainer:
    """Trainer class that trains a model and evaluates it."""

    def __init__(
        self,
        dataloader: Dataloader,
        data_processor: DataProcessor,
        model: Model,
        random_seed: int = 0,
    ) -> None:
        self.data_processor = data_processor(dataloader)
        self.model = model(self.data_processor, random_seed)

    def train(self, model_filename: str, upload_to_gcs: bool = False) -> None:
        """Train the model and save it.

        Args:
            model_filename (str):
                The filename in which the model will be saved.
            upload_to_gcs (bool, optional):
                Whether to upload the model to a GCS bucket. Defaults to False.
        """
        X_train, y_train = self.data_processor.get_train_data()

        logger.info("Training the model", data_shape=X_train.shape)
        self.model.train(X_train, y_train)

        logger.info("Saving the model", filename=model_filename, upload_to_gcs=upload_to_gcs)
        self._save_model(model_filename, upload_to_gcs)

    def _save_model(self, model_filename: str, upload_to_gcs: bool = False) -> None:
        """Save the model locally and optionally upload it to a GCS bucket.

        Args:
            model_filename (str):
                The filename in which the model will be saved.
            upload_to_gcs (bool, optional):
                Whether to upload the model to a GCS bucket. Defaults to False.
        """
        self.model.save_model(model_filename)

        if upload_to_gcs:
            logger.info("Uploading the model to GCS", filename=model_filename)
            try:
                utils.upload_to_gcs(model_filename)
            except Exception as e:
                # For simplicity, any error while uploading the model to GCS is logged but not
                # raised. This won't be the case in a real project, of course.
                logger.error("Error uploading the model to GCS", error=e)

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
            X_test, y_test = self.data_processor.get_test_data()
        else:
            if any(col in test_set.columns for col in self.test_set.cols):
                raise ValueError(f"The test set must have all these columns: {self.test_set.cols}")

            train_cols = self.data_processor.get_train_cols()
            target_col = self.data_processor.get_target_col()
            X_test = test_set[train_cols]
            y_test = test_set[target_col]

        logger.info("Evaluating the model", data_shape=X_test.shape)
        y_pred = self.model.predict(X_test)

        logger.info("RMSE", rmse=np.sqrt(mean_squared_error(y_pred, y_test)))
        logger.info("MAPE", mape=mean_absolute_percentage_error(y_pred, y_test))
        logger.info("MAE", mae=mean_absolute_error(y_pred, y_test))
