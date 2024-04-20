import psycopg2

# 数据库连接参数
DATABASE = "face_db"
USER = "postgres"
PASSWORD = "lkzxxzcsc2020"
HOST = "localhost"


# 连接数据库
def connect_db():
    conn = psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)
    return conn