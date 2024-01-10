from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment variables' settings for the API."""

    api_key: str
    api_host: str
    api_port: int
    google_application_credentials: str
    bucket_name: str
    bucket_model_path: str
    dev_mode: bool

    model_config = SettingsConfigDict(env_file="api.env")


settings = Settings()
