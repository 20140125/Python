from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.app import Settings

settings = Settings()
debug = settings.db_debug
# 创建数据库引擎
engine = create_engine('mysql+pymysql://{username}:{password}@{host}/{database}'.format(
    username=settings.db_username,
    password=settings.db_password,
    host=settings.db_host,
    database=settings.db_database
),
    echo=debug
)
# 创建数据库会话
Session = sessionmaker(bind=engine)
