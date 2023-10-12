import os

# 项目的绝对路径
project_path = os.path.dirname(os.path.dirname(__file__))
# 日志等级
mysql = {
    "host": os.getenv("SQL_HOST", ""),
    "port": int(os.getenv("SQL_PORT", "")),
    "user": os.getenv("SQL_USER", ""),
    "password": os.getenv("SQL_PASSWORD", ""),
    "database": os.getenv("DATABASE", ""),
}


__all__ = [
    "project_path",
    "mysql",
]
