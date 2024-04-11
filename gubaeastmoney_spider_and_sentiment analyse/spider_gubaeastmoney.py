#-*- codeing = utf-8 -*-
#@Time : 2024/3/29 17:26
#@Author : ZZJ
#@File : test.py
#@Software : PyCharm
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import time
import pymysql
from datetime import datetime
import re
import random

# Define database connection parameters
host = "localhost"
user = "root"
password = ""
database = ""
table_name = "gubaeastmoney_202403"

# Connect to the database
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
            print("Successfully connected to the database")
        except Exception as e:
            print(f"Connection failed: {e}")
            retries -= 1
            print(f"Retrying connection, remaining attempts: {retries}")
            if retries > 0:
                time.sleep(delay)
    return connection

# Insert data into the database
def insert_data(connection, temp_table_name, data):
    with connection.cursor() as cursor:
        # Insert data into temporary table
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {temp_table_name} ({keys}) VALUES ({values})"
        cursor.execute(sql, tuple(data.values()))
    connection.commit()

def convert_to_datetime(update_str,page_year):
    # Attempt to convert string to datetime object
    try:
        year_str = str(page_year)
        # Directly parse the date string into a datetime object using 2024
        update_time = datetime.strptime(f"{update_str}-{year_str}", "%m-%d %H:%M-%Y")
    except ValueError:
        # Handle the error if the date string is incorrect
        print("The date string is invalid.")
        update_time = None
    # Return the parsed datetime object
    return update_time

def getHTMLText(url, retries=5, backoff_factor=0.3):
    session = requests.Session()
    # Set up retry strategy
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'DNT': '1',  # Do Not Track Request Header
        'Upgrade-Insecure-Requests': '1'
    }
    try:
        r = session.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        # Generate a random float between 5 and 8
        sleep_time = random.uniform(10, 15)
        # Sleep for a random time
        time.sleep(sleep_time)
        return r.text
    except requests.exceptions.ReadTimeout:
        print("The request timed out, possibly because the server did not respond within the specified time.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"HTTP request error: {e}")
        return None

def main():
    max_page = 1000
    df = pd.read_csv('inf_stock_data.csv')
    stocklist = df.iloc[:,0].str.slice(0, 6).tolist()

    # Connect to the database
    connection = connect_to_database(host, user, password, database)
    for stock in stocklist[110:300]:
        print(f'Starting to crawl comments for {stock}')
        for i in range(1, max_page + 1):

            successful_parse = False  # Set flag to track if parsing is successful
            while not successful_parse:  # Use a while loop to allow reparsing
                url = f'https://guba.eastmoney.com/list,{stock}_{i}.html'
                html_detail = getHTMLText(url)
                if html_detail is None:
                    print(f'Page {i} of stock {stock} did not parse any content')
                    break  # If no content is parsed from the page, exit the current loop

                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(html_detail, 'html.parser')

                # Look for the <meta name="keywords"> tag
                meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
                if meta_keywords and 'content' in meta_keywords.attrs:
                    keywords_content = meta_keywords['content']  # Extract the value of the content attribute
                    print(keywords_content)  # Print the value of the content attribute

                    # And if content contains specific keywords
                    if any(keyword in keywords_content for keyword in ['Fang Zheng Securities', '601901']) and (stock != '601901'):
                        # And if content contains specific keywords
                        print("Stock keyword does not match, rest for half an hour and retry")
                        time.sleep(1800)  # Rest for 30 minutes
                        continue  # Continue the while loop, reparsing
                    successful_parse = True  # Set successful parsing flag
                else:
                    # If the meta keywords are not found or there is no content attribute
                    print(f"Page {url} did not find the appropriate meta keywords tag")

            # Find all the rows in the table with class 'listitem'
            rows = soup.find_all('tr', class_='listitem')

            one_page_data = []
            # Initialize a counter
            jump = 0
            non_march_count = 0
            # Iterate over each row and extract the required information
            for row in rows:
                update_div = row.find('div', class_='update')
                raw_time = update_div.text if update_div else 'No update info'
                update_time = convert_to_datetime(raw_time,"2024")
                # Check if the month is March
                if update_time.month != 3:
                    non_march_count += 1  # Increment the non-March record count by one
                    print('The current record is not from March')
                # Exit the loop if there are five consecutive records not from March
                if non_march_count >= 5:
                    jump = 1
                    print(f'Page {i} has five records not from March, exiting the loop')
                    break
                read_counts = row.find('div', class_='read').text
                comment_counts = row.find('div', class_='reply').text
                title_div = row.find('div', class_='title')
                title = title_div.text.strip() if title_div else 'No title'
                detail_link = title_div.a['href'] if title_div and title_div.a else 'No link'
                post_id = title_div.a['data-postid'] if title_div and title_div.a else 'No postid'  # Extracting data-postid
                author_div = row.find('div', class_='author')
                author = author_div.text.strip() if author_div else 'No author'

                print(title)
                source = 'gubaeastmoney'
                stock_index = stock
                post_id = post_id + stock_index
                data = [post_id, stock_index, read_counts, comment_counts, title, author, update_time, detail_link, source]
                one_page_data.append(data)

            for data in one_page_data:
                data_dict = dict(
                    zip(['post_id', 'stock_index', 'read_counts', 'comment_counts', 'title', 'author', 'update_time',
                         'detail_link', 'source'], data))
                try:
                    insert_data(connection, table_name, data_dict)
                except Exception as e:
                    connection = connect_to_database(host, user, password, database)
                    print(f'Data insertion error on page {i} for stock {stock}: {e}')
            print(i)

            if jump == 1:
                print(f'Finished crawling March 2024 data for stock {stock} on page {i}')
                break

            # Generate a random floating-point number between 5 and 8
            sleep_time = random.uniform(10, 15)
            # Sleep for a random amount of time
            time.sleep(sleep_time)

    # Close the database connection
    connection.close()

if __name__ == "__main__":
    main()