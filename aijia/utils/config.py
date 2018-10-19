from utils.functions import get_mysqldb_url


class Config():
    # 配置数据库
    SQLALCHEMY_DATABASE_URI = get_mysqldb_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret_key'