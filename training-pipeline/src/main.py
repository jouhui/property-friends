from src.dataloader import CsvDataloader
from src.trainer import Trainer
from src.data_processing import DataProcessor
from src.model import GradientBoostingRegressorModel

if __name__ == "__main__":
    dataloader = CsvDataloader(train_path="data/train.csv", test_path="data/test.csv")
    trainer = Trainer(
        dataloader=dataloader, data_processor=DataProcessor, model=GradientBoostingRegressorModel
    )
    trainer.train(model_filename="models/model.joblib", upload_to_gcs=True)
    trainer.evaluate()
