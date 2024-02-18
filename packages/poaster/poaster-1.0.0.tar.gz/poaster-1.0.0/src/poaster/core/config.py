import functools

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(frozen=True)

    db_path: str = "/./poaster.db"
    secret_key: str = ""
    algorithm: str = "HS256"

    @functools.cached_property
    def async_uri(self) -> str:
        return f"sqlite+aiosqlite://{self.db_path}"

    @functools.cached_property
    def uri(self) -> str:
        return f"sqlite://{self.db_path}"


settings = Settings()
