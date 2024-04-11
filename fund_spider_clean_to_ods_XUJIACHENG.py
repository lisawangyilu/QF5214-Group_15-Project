import csv
import time
import random
import requests
import traceback
from time import sleep
from fake_useragent import UserAgent
from lxml import etree
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
# Set the number of pages to crawl
page_count = 20
RETRY_TIMES=10
# Define the fund codes to crawl
# fundcodes = ['510300']

df = pd.read_excel('top100_funds.xlsx')
funds_list=df['基金代码'].to_list()
fundcodes = [fund.split('.')[0] for fund in funds_list]
print(fundcodes)


# Set headers with a random user agent
headers = {"User-Agent": UserAgent().random}
all_data=[]
# Loop through each fund code
for i in range(len(fundcodes)):
    code = fundcodes[i]
    print(f'scrapering {code}')
    full_code=funds_list[i]
    results_df = pd.DataFrame(columns=['阅读', '评论', '标题', '作者', '时间'])

    sleep(random.uniform(30, 40))
    for page_num in range(1, page_count+1):
        sleep(random.uniform(10, 15))
        for attempt in range(RETRY_TIMES+1):
            try:
                # formulate URL
                url = f'http://guba.eastmoney.com/list,of{code}.html' if page_num == 1 else f'http://guba.eastmoney.com/list,of{code}_{page_num}.html'

                response = requests.get(url, headers=headers, timeout=10)

                # parse HTML
                parse = etree.HTML(response.text)

                # extract data
                items = parse.xpath('//*[@id="articlelistnew"]/div')[1:91]
                for item in items:
                    item_info = {
                        '阅读': ''.join(item.xpath('./span[1]/text()')).strip(),
                        '评论': ''.join(item.xpath('./span[2]/text()')).strip(),
                        '标题': ''.join(item.xpath('./span[3]/a/text()')).strip(),
                        '作者': ''.join(item.xpath('./span[4]/a/font/text()')).strip(),
                        '时间': ''.join(item.xpath('./span[5]/text()')).strip()
                    }
                    results_df = results_df._append(item_info, ignore_index=True)
                break

            except Exception as e:
                print(f"An error occurred: {e}. Retrying...")
                if attempt == RETRY_TIMES - 1:
                    print("Failed after several retries.")
    results_df['fund_id'] = code
    df=results_df
    date_column = '时间'
    #guba websites do not contain information about the year, which leads to confusion about the years. Data cleaning is carried out using the original order
    # Drop rows where the date column has NA/NAN values
    df.dropna(subset=[date_column], inplace=True)
    # Check if the date column is in string format or datetime format
    if isinstance(df[date_column].iloc[0], str):
        # If it's a string, check if it starts with '02-'
        feb_index = df[df[date_column].str.startswith('02-')].index.min()
        df[date_column] = pd.to_datetime(df[date_column], format='%m-%d %H:%M', errors='coerce')
        # Replace the year with the current year
        current_year = datetime.now().year
        df[date_column] = df[date_column].apply(lambda x: x.replace(year=current_year) if pd.notnull(x) else x)

    else:
        # If it's a datetime, extract the month and check for February (2)
        df[date_column] = pd.to_datetime(df[date_column])
        feb_index = df[df[date_column].dt.month == 2].index.min()
    # Drop rows where the date column has NA/NAN values AFTER the conversion
    df.dropna(subset=[date_column], inplace=True)
    # If a February date is found, slice the DataFrame up to that date (excluding)
    if feb_index is not None and feb_index > 0:
        df = df.iloc[:feb_index]
    df.rename(columns={'阅读': 'views_count', '评论': 'comments_count', '标题': 'comment', '作者': 'author_name',
                       '时间': 'time'},
              inplace=True)
    all_data.append(df)

# Concatenating all the data frames into one
merged_df = pd.concat(all_data, ignore_index=True)
merged_df['source'] = 'gubaeastmoney'
merged_df.to_csv('merged_data_fund.csv', index=False, encoding='utf_8_sig') #local backup file


'''upload to database'''
import time
import pymysql
host='47.254.198.45',
database='qf5214',
user='user',
password='password'
table_name = "ods_comment_ef_fund"

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


def insert_data(connection, table_name, data):
    with connection.cursor() as cursor:
        # Insert data into temporary table
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table_name} ({keys}) VALUES ({values})"
        cursor.execute(sql, tuple(data.values()))
    connection.commit()



connection = connect_to_database(host, user, password, database)
i=0
while i <len(merged_df):
    data_dict=merged_df.iloc[i]
    try:
        insert_data(connection, table_name, data_dict)
        i+=1
    except Exception as e:
        connection = connect_to_database(host, user, password, database)
        print(f'第{i}行数据入表错误: {e}')




sleep_time = random.uniform(10, 15)
time.sleep(sleep_time)
connection.close()