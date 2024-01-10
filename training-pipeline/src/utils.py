from google.cloud import storage
from google.oauth2.service_account import Credentials

from .config import settings


def upload_to_gcs(filename: str) -> None:
    """Upload a file to Google Cloud Storage.

    Args:
        filename (str): The filename of the file to upload.
    """
    credentials = Credentials.from_service_account_file(
        f"credentials/{settings.google_application_credentials}"
    )
    client = storage.Client(credentials=credentials)
    bucket = client.get_bucket(settings.bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)
