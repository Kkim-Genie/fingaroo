from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    LLM_MODEL_BASE: str = "HCX-005"
    LLM_MODEL_HIGH: str = "HCX-007"
    NAVER_SEARCH_URL: str = "https://openapi.naver.com/v1/search/news.json"
    NAVER_CLIENT_ID: str = ""
    NAVER_CLIENT_SECRET: str = ""
    NAVER_STATE: str =  ""
    DART_API_KEY: str = ""
    SUPABASE_USER: str = ""
    SUPABASE_PASSWORD: str = ""
    SUPABASE_HOST: str = ""
    CLOVASTUDIO_API_KEY: str = ""
    JWT_ACCESS_SECRET_KEY: str = ""
    JWT_REFRESH_SECRET_KEY: str = ""
    DATA_GO_API_KEY: str = ""

@lru_cache
def get_settings():
    return Settings()