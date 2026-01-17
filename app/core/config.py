from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, ValidationInfo, field_validator



class Settings(BaseSettings):
    BOT_TOKEN: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: str | None = None
    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: str | None, info: ValidationInfo) -> str:
        if isinstance(v, str):
            return v
        values = info.data
        return str(PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        ))
    
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30

    MODEL_TYPE: str = ""  # "local" or "gen_ai"

    LOCAL_MODEL_URL: str = ""
    LOCAL_MODEL_NAME: str = ""

    GEN_AI_API_KEY: str = ""
    GEN_AI_MODEL_NAME: str = ""

settings = Settings()