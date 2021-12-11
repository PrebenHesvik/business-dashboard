from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool
    secret_key: str
    sqlalchemy_database_uri: str
    admin: str
    admin_password: str

    class Config:
        env_file = '.env'


settings = Settings()
