from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bucket_name: str
    google_application_credentials: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
