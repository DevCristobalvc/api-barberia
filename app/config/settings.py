from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    supabase_url: str
    supabase_key: str
    supabase_service_key: str
    openai_api_key: str
    redis_url: str = "redis://localhost:6379"
    environment: str = "development"
    openai_model: str = "gpt-4o-mini"


settings = Settings()
