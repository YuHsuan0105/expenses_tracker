import os

import pymysql

# get mysql connection
def get_conn() -> pymysql.connections.Connection:
    return pymysql.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PWD'],
        database=os.environ['DB_NAME']
    )

def insert(table: str, user: int, money: int, category: str) -> None:
    sql = (
        f"insert into {table}(user_id,money,category,created_at) "
        f"values('{user}',{money},'{category}',CURRENT_DATE);"
    )
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
