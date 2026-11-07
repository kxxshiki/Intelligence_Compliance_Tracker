from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Intelligent Cyber Compliance Tracker"
    app_env: str = "development"
    database_url: str = "sqlite:///./cyber_compliance.db"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen8:3b"
    embedding_model: str = "all-MiniLM-L6-v2"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
