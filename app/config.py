import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    model: str = "meta-llama/llama-3.1-8b-instruct:free"
    csv_file_path: str = "sources.csv"
    
    class Config:
        env_file = ".env"

settings = Settings()
