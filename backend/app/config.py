from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field

class Settings(BaseSettings):
    model_config = ConfigDict(extra="allow", env_file=".env")

    PROJECT_NAME: str = "HiveMind Runtime"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///hivemind.db",
        description="Database connection string"
    )
    DEFAULT_LEASE_TTL_SECONDS: int = 15
    GATEWAY_WS_URL: str = "ws://localhost:4000"

settings = Settings()
