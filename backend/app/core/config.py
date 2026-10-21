from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    amt_env: str = "development"
    amt_debug: bool = True
    amt_host: str = "127.0.0.1"
    amt_port: int = 8010
    amt_cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    amt_rate_limit_requests: int = 240
    amt_rate_limit_window_seconds: int = 60
    amt_provider_timeout_seconds: int = 120

    # ---- paid providers ----
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    xai_api_key: str = ""
    mistral_api_key: str = ""
    deepseek_api_key: str = ""
    together_api_key: str = ""
    fireworks_api_key: str = ""

    # ---- free-tier providers ----
    gemini_api_key: str = ""
    groq_api_key: str = ""
    cerebras_api_key: str = ""
    openrouter_api_key: str = ""
    opencode_zen_api_key: str = ""
    nvidia_api_key: str = ""
    zai_api_key: str = ""
    siliconflow_api_key: str = ""
    cloudflare_api_key: str = ""
    custom_api_key: str = ""

    # ---- base url overrides ----
    openai_base_url: str = ""
    xai_base_url: str = "https://api.x.ai/v1"
    gemini_base_url: str = ""
    groq_base_url: str = ""
    cerebras_base_url: str = ""
    openrouter_base_url: str = ""
    opencode_zen_base_url: str = ""
    nvidia_base_url: str = ""
    zai_base_url: str = ""
    siliconflow_base_url: str = ""
    mistral_base_url: str = ""
    deepseek_base_url: str = ""
    together_base_url: str = ""
    fireworks_base_url: str = ""
    cloudflare_base_url: str = ""
    ollama_base_url: str = "http://localhost:11434/v1"
    lmstudio_base_url: str = "http://localhost:1234/v1"
    custom_base_url: str = ""

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.amt_cors_origins.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.amt_env.lower() == "production"

    @property
    def project_root(self) -> Path:
        return BASE_DIR.parent


@lru_cache
def get_settings() -> Settings:
    return Settings()
