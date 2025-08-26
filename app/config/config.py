from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):

    app_name: str = "Airport API"
    debug: bool = False

    db_dsn: str

    redis_dsn: str

    rabbit_dsn: str

    jwt_secret: str
    jwt_algorithm:str = "HS256"
    jwt_access_expires: int = 3600
    jwt_refresh_expires: int = 259200

    model_config = SettingsConfigDict(
        env_file= ".env",
        env_file_encoding= "utf-8",
        from_attributes=True
    )

settings = Settings()