import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    user_service_url: str = os.environ['USER_SERVICE_URL']
    account_service_url: str = os.environ['ACCOUNT_SERVICE_URL']
    credit_service_url: str = os.environ['CREDIT_SERVICE_URL']
    exchange_service_url: str = os.environ['EXCHANGE_SERVICE_URL']
    rabbitmq_account_host: str = os.environ['RABBITMQ_ACCOUNT_HOST']
    rabbitmq_account_port: str = os.environ['RABBITMQ_ACCOUNT_PORT']
    rabbitmq_account_login: str = os.environ['RABBITMQ_ACCOUNT_LOGIN']
    rabbitmq_account_password: str = os.environ['RABBITMQ_ACCOUNT_PASSWORD']
    transfer_queue_name: str = os.environ['TRANSFER_QUEUE']


settings = Settings()
