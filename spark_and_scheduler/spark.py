#-*- codeing = utf-8 -*-
#@Time : 2024/4/10 1:51
#@Author : ZZJ
#@File : spark2.py
#@Software : PyCharm

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col
import os
from datetime import datetime

# 定义源到数据库连接信息的映射关系
source_to_db_config = {
    "gubaeastmoney": {
        "host": "localhost",
        "user": "root",
        "password": "19961012",
        "database": "yqfx",
        "word_count_table": "gubaeastmoney_word_counts",
        "original_data_table": "gubaeastmoney_original_data"
    },
    "othersource": {
        "host": "otherhost",
        "user": "otheruser",
        "password": "otherpassword",
        "database": "otherdatabase",
        "word_count_table": "othertable_202403_word_counts",
        "original_data_table": "othertable_202403_original_data"
    }
    # 这里可以添加更多的源和数据库连接信息
}
def create_spark_session(app_name):
    # Set the path to the MySQL Connector/J .jar file
    jdbc_driver_path = "file:///E:/mysql-connector-j-8.3.0/mysql-connector-j-8.3.0.jar"  # Update with the actual .jar file name if necessary
    return SparkSession.builder \
        .appName(app_name) \
        .config("spark.jars", jdbc_driver_path) \
        .getOrCreate()

def get_csv_files_for_date(data_dir, date_str):
    return [os.path.join(data_dir, file) for file in os.listdir(data_dir)
            if file.endswith('.csv') and date_str in file]

def process_file(spark, file_path):
    df = spark.read.option("encoding", "UTF-8").csv(file_path, header=True)
    sources = df.select("source").distinct().rdd.flatMap(lambda x: x).collect()

    for source in sources:
        process_source(df, file_path, source)


def process_source(df, file_path, source):
    # Filter the dataframe for the current source
    df_source = df.filter(col("source") == source)

    # Process the word counts
    word_counts = df_source.select(explode(split(col("title"), "\\s+")).alias("word")) \
        .groupBy("word").count().sort("count", ascending=False)

    # Get connection parameters
    connection_params = get_database_connection_parameters(source)

    # Write the word counts to the database
    word_counts_table_name = source_to_db_config[source]['word_count_table']
    write_to_db(word_counts, word_counts_table_name, connection_params)

    # Write the original data to the database
    original_data_table_name = source_to_db_config[source]['original_data_table']
    write_to_db(df_source, original_data_table_name, connection_params)

# 获取数据库连接URL
def get_jdbc_url(host, database):
    return f"jdbc:mysql://{host}:3306/{database}"

# 获取数据库连接参数
def get_database_connection_parameters(source):
    if source in source_to_db_config:
        db_config = source_to_db_config[source]
        return {
            "url": get_jdbc_url(db_config['host'], db_config['database']),
            "properties": {
                "user": db_config['user'],
                "password": db_config['password'],
                "driver": "com.mysql.cj.jdbc.Driver"
            }
        }
    else:
        raise ValueError(f"No database configuration found for source: {source}")

# 将DataFrame写入数据库到指定表
def write_to_db(df, table_name, connection_params):
    df.write.jdbc(url=connection_params["url"], table=table_name, mode="overwrite", properties=connection_params["properties"])

def main():
    # Initialize Spark session
    spark = create_spark_session("Word Frequency Analysis by Source")

    # Set the data directory path
    data_dir = "sparkdata"

    # Get the current date string in the same format as expected in the filenames
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Get all CSV files in the data directory that contain the current date
    csv_files = get_csv_files_for_date(data_dir, current_date)

    for file_path in csv_files:
        process_file(spark, file_path)

    # Stop the Spark session
    spark.stop()

    print('ok')

if __name__ == "__main__":
    main()