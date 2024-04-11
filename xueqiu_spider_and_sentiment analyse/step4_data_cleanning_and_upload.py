import time
import pymysql
import pandas as pd

# ============database setting==================
host='47.254.198.45',
database='qf5214',
user='user',
password='password'

# 要操作的表名
# table_name = "ods_comment_SB_stock"

# ===================func======================
# 连接数据库
def connect_to_database(host, user, password, database, retries=5, delay=5):
    connection = None
    while not connection and retries > 0:
        try:
            connection = pymysql.connect(host=host,
                                         user=user,
                                         password=password,
                                         database=database,
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
            print("已成功连接到数据库")
        except Exception as e:
            print(f"连接失败：{e}")
            retries -= 1
            print(f"重试连接，剩余尝试次数：{retries}")
            if retries > 0:
                time.sleep(delay)
    return connection


def fetch_data_from_time(connection, table_name, first_analyzed_time, last_analyzed_time):
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM {table_name} WHERE created_at > '{last_analyzed_time}' OR created_at < '{first_analyzed_time}'"
        cursor.execute(sql)
        result = cursor.fetchall()
    return result


# ===================write in database======================

input = pd.read_csv('final_loss.csv')

connection = connect_to_database(host, user, password, database)

for data in input:
        data_dict = dict(zip(['post_id', 'stock_index', 'read_counts', 'comment_counts', 'title', 'author', 'update_time','detail_link','source'], data))
            try:
                #数据插入table_name表里
                insert_data(connection, table_name, data_dict)
            except Exception as e:
                connection = connect_to_database(host, user, password, database)
                print(f'股票{stock}第{i}页数据入表错误: {e}')
        print(i)

        # 生成一个 5 到 8 之间的随机浮点数
        sleep_time = random.uniform(10, 15)
        # 睡眠随机时间
        time.sleep(sleep_time)

# 最后要记得关闭数据库连接
connection.close()