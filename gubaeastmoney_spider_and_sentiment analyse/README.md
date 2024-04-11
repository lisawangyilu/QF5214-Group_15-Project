Eastmoney Comment Analysis
This project includes a web scraper to collect comments from the Eastmoney forum and two alternative methods for sentiment analysis of the collected data: one using Baidu's sentiment analysis API and another using OpenAI's GPT model.

Prerequisites
Python 3.x
MySQL Server (Local or remote)
Baidu API account (for Baidu API method)
OpenAI API account (for OpenAI method)
Installation
Install the required Python packages using pip:

pip install pandas numpy requests beautifulsoup4 pymysql openai
Set up a MySQL database and create the required tables as specified in the scripts.

Usage
Part 1: Web Scraping
The web scraping script collects comments from the Eastmoney forum. Before running it, you need to:

Update the script with your MySQL database credentials.
Specify the stock codes and date ranges for which you wish to collect comments.
Run the script to start scraping data. The collected data will be stored in the MySQL database in the gubaeastmoney table.
Part 2: Sentiment Analysis
Method 1: Baidu API Sentiment Analysis
To use the Baidu API for sentiment analysis:

Obtain your Baidu API credentials (APP_ID, API_KEY, SECRET_KEY).
Update the Baidu sentiment analysis script with your credentials and database connection parameters.
Run the script. It will read titles from the gubaeastmoney table, perform sentiment analysis, and insert the results into the gubaeastmoney_sentiment table.
Method 2: OpenAI GPT Sentiment Analysis
To use OpenAI's GPT model for sentiment analysis:

Set your OpenAI API key in the environment variable or directly in the script.
Configure the database connection parameters in the OpenAI sentiment analysis script.
Run the script. It will process comments in batches, perform sentiment analysis, and store the results in the gubaeastmoney_202403_ana table.
Database Schema
The database should contain the following tables with the appropriate schemas:

For scraped data: gubaeastmoney
For Baidu API results: gubaeastmoney_sentiment
For OpenAI GPT results: gubaeastmoney_202403_ana
Configuration
All scripts include error handling and retry logic for robust execution.
The OpenAI method has a loop to continuously process new data and is set up to run daily.
Adjust the BATCH_SIZE in the OpenAI method to control the number of comments processed in each batch.
Limitations and Disclaimer
The sentiment analysis methods are based on AI models and may not always provide perfect accuracy.
The web scraping script must be used in compliance with Eastmoney's terms of service.
Users should respect data privacy and copyright laws when using these scripts.
The provided scripts are for educational and research purposes only.
Support
For any issues or questions, please open an issue on the project's repository, and a maintainer will assist you.