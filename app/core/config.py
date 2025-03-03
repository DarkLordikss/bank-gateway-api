import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    user_service_url: str = os.environ['USER_SERVICE_URL']
    account_service_url: str = os.environ['ACCOUNT_SERVICE_URL']


settings = Settings()
