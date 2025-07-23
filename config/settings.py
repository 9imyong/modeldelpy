from pydantic import BaseSettings

class Settings(BaseSettings):
    ADMIN_USERNAME: str
    ADMIN_PASSWORD_HASH: str
    CSRF_SECRET: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()