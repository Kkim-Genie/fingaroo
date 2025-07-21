from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    OPENAI_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    GOOGLE_CLOUD_PROJECT: str = ""
    GOOGLE_GENAI_USE_VERTEXAI: bool = True
    GOOGLE_CLOUD_LOCATION: str = "us-central1"
    GOOGLE_APPLICATION_CREDENTIALS: str = ""
    LLM_MODEL: str = "gemini-2.5-flash-lite-preview-06-17"
    NAVER_SEARCH_URL: str = "https://openapi.naver.com/v1/search/news.json"
    NAVER_CLIENT_ID: str = ""
    NAVER_CLIENT_SECRET: str = ""
    DART_API_KEY: str = ""
    SUPABASE_USER: str = ""
    SUPABASE_PASSWORD: str = ""
    SUPABASE_HOST: str = ""
    API_URL: str = "http://localhost:8000"


@lru_cache
def get_settings():
    return Settings()