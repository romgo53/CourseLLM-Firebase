# settings.py
import os
from pydantic import Field
from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.example")

    port: int = Field(default=8000, alias="PORT")
    log_level: str = Field(default="info", alias="LOG_LEVEL")
    lm_model: str = Field(default="gemini/gemini-2.5-flash", alias="LM_MODEL")
    lm_api_key: str = Field(default="", alias="LM_API_KEY")
    firebase_service_account: dict = Field(default={}, alias="FIREBASE_SERVICE_ACCOUNT_JSON")
    test_auth_token: str = Field(default="", alias="TEST_AUTH_TOKEN")

 