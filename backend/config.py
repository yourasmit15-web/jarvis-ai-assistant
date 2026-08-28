import os
from dataclasses import dataclass


@dataclass
class Settings:
    app_name: str = os.getenv("APP_NAME", "RAGHUVIR API")
    assistant_name: str = os.getenv("RAGHUVIR_NAME", "RAGHUVIR")
    allowed_origins: list[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")


settings = Settings()
