import os
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENV", "development")
    env_file: str = f".env.{ENVIRONMENT}"
    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8"
    )
    
    # App
    DEBUG: bool = False
    APP_NAME: str = "Smm TMA"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = SecretStr("secret-key")
    
    # Database
    DATABASE_NAME: str = "database"
    DATABASE_HOST: str = "localhost"
    DATABASE_USER: str = "user"
    DATABASE_PASSWORD: SecretStr = SecretStr("password")
    DATABASE_ECHO: bool = False
    DATABASE_PORT: int = 5432

    # Ton
    TON_API_KEY: SecretStr = SecretStr("your-ton-api-key") # https://tonconsole.com/
    TON_CENTER_API_KEY: SecretStr = SecretStr("your-ton-center-api-key") # https://toncenter.com/
    TON_WALLET_MNEMONIC: SecretStr = SecretStr("your-ton-wallet-mnemonic")
    
    # Bot
    BOT_TOKEN: SecretStr = SecretStr("your-bot-token")

    # Smm
    SOC_PROOF_API_KEY: SecretStr = SecretStr("your-soc-proof-api-key")  # MAIN API KEY
    
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD.get_secret_value()}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )


settings = Settings()