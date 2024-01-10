import joblib
from google.cloud import storage
from google.oauth2.service_account import Credentials

from .config import settings


def load_model_from_gcs():
    """Load the model from Google Cloud Storage."""
    credentials = Credentials.from_service_account_file(
        f"credentials/{settings.google_application_credentials}"
    )

    client = storage.Client(credentials=credentials)
    bucket = client.get_bucket(settings.bucket_name)

    blob = bucket.blob("models/model.joblib")
    blob.download_to_filename("model.joblib")
    model = joblib.load("model.joblib")
    return model
