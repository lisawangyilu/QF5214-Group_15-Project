#-*- codeing = utf-8 -*-
#@Time : 2023/4/19 23:43
#@Author : ZZJ
#@File : test_ai3.py
#@Software : PyCharm
import pymysql
import pandas as pd
import openai
import os
import json
import requests
import time

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = ""
openai.api_key = os.getenv("OPENAI_API_KEY")

# Connect to the database
def connect_to_database(host, user, password, database):
    connection = pymysql.connect(host=host,
                                 user=user,
                                 password=password,
                                 database=database,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

# Insert data into the database
def insert_data(connection, data):
    with connection.cursor() as cursor:
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO gubaeastmoney_202403_ana ({keys}) VALUES ({values})"
        cursor.execute(sql, tuple(data.values()))
    connection.commit()

# Classify the sentiment of a comment
def classify_comment(combined_comments):

    messages = [
        {"role": "system", "content": "You are an AI assistant that helps users judge the sentiment of stock bar comments."},
        {"role": "user",
         "content": f"Please analyze the sentiment of this comment from the perspective of a professional stock investor: {combined_comments}, and strictly output the result in the following format based on the sentiment analysis: 'positive', 'negative', 'neutral'. If undetermined, output 'fail'. Note: Most comments fundamentally discuss stock price movements."}
    ]

    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": 150,
        "temperature": 0.2,
        "n": 1,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}",
    }

    max_retries = 10  # Set the maximum number of retries
    retries = 0

    while retries <= max_retries:
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                data=json.dumps(data)
            )
            response.raise_for_status()  # Check for HTTP errors
            break
        except requests.exceptions.RequestException as e:
            retries += 1
            print(f"Request failed, retrying... ({retries}/{max_retries})")
            time.sleep(5)
            if retries > max_retries:
                print("Maximum number of retries reached, stopping retry.")
                raise e

    response_json = response.json()
    if 'choices' in response_json:
        result = response_json['choices'][0]['message']['content'].strip()
    else:
        result = "Error: No choices found in response."

    return result


# Define database connection parameters
host = ""
user = ""
password = ""
database = ""

# Set the batch size for processing data
BATCH_SIZE = 100

while True:
    # Connect to the database
    connection = connect_to_database(host, user, password, database)

    # Initialize the offset
    offset = 0

    while True:
        # Construct SQL query, using LIMIT and OFFSET clauses for pagination
        sql = "SELECT * FROM gubaeastmoney_202403 LIMIT %s OFFSET %s"

        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(sql, (BATCH_SIZE, offset))
            batch_data = cursor.fetchall()

        # If there is no more data, exit the loop
        if not batch_data:
            break

        # Process each row of data
        for row in batch_data:
            try:
                combined_comment = row['title']
                result = classify_comment(combined_comment)

                row['sentiment'] = result

                # Insert the result into another table
                insert_data(connection, row)
            except Exception as e:
                print(f'Error analyzing data: {e}')
                continue

        # Update the offset to move to the next batch
        offset += BATCH_SIZE

    # Close the database connection
    connection.close()

    # Schedule to run daily (24 hours * 60 minutes * 60 seconds)
    time.sleep(24 * 60 * 60)








