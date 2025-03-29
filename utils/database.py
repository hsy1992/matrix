import pymysql
from dbutils.pooled_db import PooledDB
from conf import MYSQL_CONF

# 创建连接池
pool = PooledDB(
    creator=pymysql,  # 使用 PyMySQL 驱动
    maxconnections=5,  # 最大连接数
    mincached=2,  # 初始化时创建的空闲连接数量
    maxcached=3,  # 连接池中允许的最大空闲连接数量
    blocking=True,  # 达到最大连接数时是否等待
    host=MYSQL_CONF['host'],
    port=MYSQL_CONF['port'],
    user=MYSQL_CONF['username'],
    password=MYSQL_CONF['password'],
    database=MYSQL_CONF['database'],
    charset="utf8mb4",
    autocommit=MYSQL_CONF['auto_commit']
)

# 从连接池获取连接
connection = pool.connection()


def get_cursor():
    return connection.cursor()


def close_connection():
    return connection.close()

