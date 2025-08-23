import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    bot_token: str
    admin_chat_id: str
    base_dir: str = os.path.dirname(os.path.dirname(__file__))

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_DRIVER: str

    APP_NAME: str
    ENVIRONMENT: str
    LOG_LEVEL: str
    LOG_FORMAT: str

    @property
    def db_url(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def send_msg_url(self, text: str) -> str:
        return (f"https://api.telegram.org/bot{self.bot_token}/"
                f"sendMessage?chat_id={self.admin_chat_id}&text={text}")

    class Config:
        env_file = ".env"



settings = Settings()