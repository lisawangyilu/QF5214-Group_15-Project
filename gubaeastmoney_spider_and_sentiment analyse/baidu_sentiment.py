#-*- codeing = utf-8 -*-
#@Time : 2024/4/3 13:00
#@Author : ZZJ
#@File : baidu_sentiment.py
#@Software : PyCharm

import pandas as pd
import numpy as np
import time
import pymysql
from aip import AipNlp

# Initialize AipNlp with your credentials
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

# Database connection parameters
DB_HOST = 'localhost'
DB_USER = 'username'
DB_PASS = 'password'
DB_NAME = 'yqfx'

# Function to create a database connection
def create_connection():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)

# Function to read the gubaeastmoney table
def read_table(table_name):
    conn = create_connection()
    try:
        sql_query = f"SELECT * FROM {table_name};"
        return pd.read_sql_query(sql_query, conn)
    finally:
        conn.close()

# Function to insert the DataFrame back into the database
def insert_into_table(df, table_name):
    conn = create_connection()
    cursor = conn.cursor()
    placeholders = ', '.join(['%s'] * len(df.columns))
    columns = ', '.join(df.columns)
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    try:
        for i, row in df.iterrows():
            cursor.execute(sql, tuple(row))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

# Function for sentiment analysis
def posi_or_nega(comment, sleep_time, max_retries=5):
    retry_count = 0
    while retry_count < max_retries:
        try:
            time.sleep(sleep_time)
            response = client.sentimentClassify(comment)
            posi_prob = response['items'][0]['positive_prob']
            nega_prob = response['items'][0]['negative_prob']
            print(f'{comment}分析完成')

            if posi_prob > 0.7:
                return 1
            elif nega_prob > 0.7:
                return -1
            else:
                return 0
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")
            retry_count += 1
            continue
    print(f'{comment}分析失败')
    return np.nan  # Return NaN if all retries fail

# Read the data from the gubaeastmoney table
gubaeastmoney_df = read_table('gubaeastmoney')

# Apply the sentiment analysis to the 'title' column
gubaeastmoney_df['sentiment'] = gubaeastmoney_df['title'].apply(
    lambda comment: posi_or_nega(comment, sleep_time=0.5, max_retries=5)
)

# Insert the DataFrame into the gubaeastmoney_sentiment table
insert_into_table(gubaeastmoney_df, 'gubaeastmoney_sentiment')

print("Data with sentiment scores stored in 'gubaeastmoney_sentiment' table.")

