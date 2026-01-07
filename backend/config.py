from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Sightline AI"
    debug: bool = True 
    allowed_origins: list[str] = ["*"]

settings = Settings()