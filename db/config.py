from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str
    app_email: str
    app_username: str
    db_host: str
    db_username: str
    db_password: str
    db_port: int
    db_connection: str
    db_database: str

    class Config:
        # 设置需要识别的 .env 文件
        env_file = '.env'
        # 设置字符编码
        env_file_encoding = 'utf-8'


settings = Settings()
