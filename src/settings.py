from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE: str
    DB_USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    DB_NAME: str
    BOT_TOKEN: str
    BASE_DIR: str = Path.cwd()
    SYNC_DATABASE: str

    class Config:
        env_file = ".env", "../.env"

    def get_database_url(self) -> str:
        return (
            f"{self.DATABASE}://"
            f"{self.DB_USER}:"
            f"{self.PASSWORD}@"
            f"{self.HOST}:"
            f"{self.PORT}/"
            f"{self.DB_NAME}"
        )

    def get_test_database_url(self) -> str:
        return (
            f"{self.DATABASE}://"
            f"{self.DB_USER}:"
            f"{self.PASSWORD}@"
            f"{self.HOST}:"
            f"{self.PORT}/"
            f"test_{self.DB_NAME}"
        )

    def get_sync_test_database_url(self) -> str:
        return (
            f"{self.SYNC_DATABASE}://"
            f"{self.DB_USER}:"
            f"{self.PASSWORD}@"
            f"{self.HOST}:"
            f"{self.PORT}/"
            f"test_{self.DB_NAME}"
        )


settings = Settings()
