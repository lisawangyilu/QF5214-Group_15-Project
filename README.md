# QF5214-Group_15-Project
# Stock Market Dashboard Project Report

## Abstract
This report presents the development process and operational details of a stock market dashboard designed to combine quantitative financial data with qualitative sentiment analysis, thereby providing investors with a holistic view of market conditions. The dashboard serves as a tool for investors to make informed decisions by examining both numerical market data and the prevailing public sentiment towards the top stocks in the market.

## Problem Statement
After the Chinese stock market's steep decline in February and March, investors face a dilemma: has market sentiment bottomed out, signaling a time to buy the dip? If news headlines are overwhelmingly positive yet stock forum sentiments are bleak, it could signal an undervalued market ripe for investment. However, sifting through forums for individual comments is a time-consuming and inefficient process, and one might miss out on crucial sentiment indicators. Enter our dashboard, a fusion of real-time financial data and sentiment analysis, designed for the modern stock market. It navigates through numerical trends and investor psychology, offering a holistic view that guides investment strategies. This tool is a game-changer for investors aiming to make informed decisions in a fluctuating market.

## Introduction

The purpose of the dashboard is to provide a nuanced view of the stock market by integrating quantitative financial data with sentiment analysis. 

The development of this dashboard used the following tools and data sources:

- **Quantitative Financial Data**: Sourced from the Wind API, which offers extensive financial data for market analysis.

- **Sentiment Data**:
  Gained through Python-based web scraping
  - **Investor Sentiment**: Gained investor comments from the Guba and Snowball forums, focusing on the CSI 300 index stocks.
  - **Fund Sentiment**: Captures broader market sentiment commentary from the top 100 funds in China from Guba forums, reflecting macro investor sentiment.
  - **News Sentiment**: Collected from Guba financial news publications to incorporate objective sentiment influences on the market.

- **Sentiment Analysis Model**: Utilizes Baidu's Large Language Model (LLM) API for sentiment judgement, chosen for its accessibility and cost-effectiveness despite slower processing times.

- **Data Processing and ETL**: Carried out with Python to ensure efficient data extraction, transformation, and loading into the system.

- **Database and Cloud Integration**: Managed via cloud-based SQL databases to facilitate data handling and collaboration.

- **Visualization and Dashboard Interface**: Constructed with Power BI for its dynamic data visualization capabilities, enhancing the interactive experience for users.

## Dataset Description

The datasets for this project are multi-faceted, encompassing both financial data and sentiment data:

- **Financial Data**: Sourced from the Wind API, this dataset includes daily stock prices, trading volumes, and holder information. Key financial metrics, such as stock returns, are computed to establish a foundation for quantitative analysis. Additionally, we obtain detailed stock information, including the `industries` stocks belong to and `hot concepts` they are associated with. This information serves as vital dimensions for subsequent data aggregation and analysis.
  
- **Sentiment Data**: Extracted using Python web scrapers, this includes investor comments from Guba and Snowball, and news content related to stocks and funds. The sentiment is analyzed for positive or negative emotions using Baidu's LLM.

- **Metrics Definition**: Metrics are defined by a combination of time periods (e.g., last 1 day), entities (stocks, funds), and data types (daily return, comment). Derived metrics are created based on these definitions, such as 'last_7_days_stock_positive_number_comment' indicating the count of positive comments over the past week.
![metrics](images/metrics.jpg)

## Data Architecture and Data Pipeline

The stock market dashboard relies on a robust data architecture and pipeline designed for efficient data flow from source to presentation. The architecture is structured into several key layers, each serving a pivotal role in the processing and analysis of data.
![modeling](images/data_modeling.jpg)

### Data Sources
The foundation of our dashboard is built upon data acquired from diverse sources:
- **Wind API**: Provides a wealth of financial data points, including stock information and trading activities.
- **Web Crawlers**: These are utilized to gather sentiment data from various financial websites, capturing the mood and opinions of the market participants.

### ODS
This layer serves as the staging area for raw data:
- It contains tables for the initial storage of stock information , stock market data and sentiment data.


### DWD and DIM
After the data is collected, it goes through an ETL process and is loaded into our Data Warehouse, which has two components:
- **DWD**: Stores the detailed, atomic-level data. Integrates the `dt` field in all fact tables for data governance.
  - **Price and Volume Domain**: Here, we maintain the granularity at the daily level for each stock. The `dwd_market_price_di` fact table stores this daily price and volume information, providing a detailed view of market activities.
  - **Sentiment Domain**: This domain differentiates between stocks and funds to provide a focused view of market sentiment. 
    - Fact tables for sentiment are dedicated to stock sentiment (`dwd_stock_sentiment_di`) and fund sentiment (`dwd_fund_sentiment_di`), where each record corresponds to sentiment data for individual stocks and funds, respectively.
    - Sentiment cleansing and emotion tagging are critical processes completed in this layer. We standardize and clean the sentiment data from various sources before applying Baidu's LLM for emotion analysis, resulting in sentiment tags that classify data as positive, negative, or neutral. This enrichment allows for sophisticated sentiment-based insights into market trends.

- **DIM**: Includes dimension tables such as `dim_stock_info` and `dim_date_info`, which are used to add context to the facts through attributes like dates, stock indices, and industry sectors.

### DWS
This layer facilitates business intelligence and analysis:
- It includes tables that have been specifically designed based on business requirements. This includes summarizing data on dimensions such as time (e.g., daily aggregates), industry, and sentiment (e.g., overall market sentiment, sentiment by industry).
- This aggregation approach within the DWS lays the groundwork for insightful analytics, allowing for the synthesis of complex data into understandable and useful business metrics.

### ADS
The ADS is where the curated data for final presentation is stored:
- This includes tables like `ads_stock_ind_return_comment_1d`. These are constructed to feed customized metrics directly into the dashboard.

### Data Pipeline
The transformation of raw data into insights is a multi-stage process:
1. **Extraction**: We pull data from the Wind API and web via crawlers.
2. **Transformation**: Raw data undergoes cleaning, normalization, and enrichment within the DWD to fit our analytical schema.
3. **Loading**: Data is then loaded into DWD for detail storage and DIM for additional context.
4. **Processing**: In DWS, data is aggregated and analyzed based on business needs to provide a clearer view for data users.
5. **Presentation**: The ADS feeds into the dashboard, which visualizes the data, offering an interactive and insightful interface for users.

Each stage of this pipeline is designed to ensure data integrity and relevance, culminating in a powerful tool that provides comprehensive market insights.

Following is a detailed diagram that illustrates the multi-tiered data architecture of our stock market dashboard. This diagram provides a visual overview of the various components in our data pipeline, from the source data to the presentation layer.
![4-Tier Data Architecture](images/4_tier_architecture.jpg)

## Implementation
#### Details on the API integration and web scraping process

- **Baidu AI API Usage Instructions**

1. Prepare the Necessary API Information: In the code, fill in your APP_ID, API_KEY, and SECRET_KEY. These are the credentials required when using Baidu's sentiment analysis service, obtainable by registering on Baidu AI Open Platform and creating the relevant application.
2. Instantiate the AI NLP Client: With the prepared APP_ID, API_KEY, and SECRET_KEY, create an instance of AipNlp.
3. Read Text Data: The script will read data from a dataframe containing the text to be processed.
4. Perform Sentiment Analysis on Each Line of Text: For each non-blank line of text in the dataframe, use the sentimentClassify method of the AipNlp instance to call the API and obtain sentiment analysis results.

- **Introduction to Baidu AI Sentiment Analysis Tool**

1. Baidu AI Open Platform's sentiment analysis capability is developed based on their PaddlePaddle deep learning framework. This functionality is part of the Senta project, offering powerful sentiment analysis tools based on pretrained models like ERNIE and RoBERTa, suitable for various sentiment analysis tasks.
2. Model Principle: Baidu's sentiment analysis models leverage the PaddlePaddle deep learning platform technology. The underlying models—ERNIE and RoBERTa—have been fine-tuned for sentiment analysis to understand and classify emotional nuances in the text. These models are trained on large datasets and can effectively recognize positive, negative, and neutral emotions.

- **Challenges Encountered in Web Scraping**

1. When using the request package to access the Dongfang Fortune website forums, the site returns a 403 Forbidden error, indicating failed access. The error message \['&lt;html&gt;\\r\\n&lt;head&gt;&lt;title&gt;403 Forbidden&lt;/title&gt;&lt;/head&gt;\\r\\n&lt;body&gt;\\r\\n&lt;center&gt;&lt;h1&gt;403 Forbidden&lt;/h1&gt;&lt;/center&gt;\\r\\n&lt;hr&gt;&lt;center&gt;Microsoft-IIS/10.0&lt;/center&gt;\\r\\n&lt;/body&gt;\\r\\n&lt;/html&gt;\\r\\n'\] suggests that the website has identified the Python access as an automated script request, thus denying access to the IP.
2. Initially, the process of scraping the website source code worked normally with automatic page redirection and scraping. However, the initial scraping results showed garbled data, with homogeneous and mismatched repetitive information. This issue is considered to be the website detecting unusual user access, perceiving the IP access frequency as too fast for human-like behavior, hence employing anti-scraping measures like returning garbled data.

- **Solutions to Problems**

1. For the first issue, resolve it by setting the User-Agent parameter in the request header. By default, requests sent using requests are set with a User-Agent of 'python-requests/version', which can easily be recognized by servers as coming from an automated script, not a regular user's browser. Example code:
    1. url = '<https://example.com>'
    2. headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    3. response = requests.get(url, headers=headers)
2. For the second issue, consider extending the interval between accesses to reduce the access frequency. Possible solutions include:
    1. Set cooling time, decrease frequency:
        1. time.sleep
        2. Set implicit waits, for example: wait1.until(lambda driver: driver.find_element_by_xpath("//p\[@id='link-report'\]/span")) to ensure the page fully loads before scraping.
    2. Use proxy IP access from an IP pool.

#### Description of the sentiment analysis model

- The model consists of two parts: the sentiment analysis module and the result integrity judgment module.
- Sentiment Analysis Module Logic:

1. If the positive probability (positive_prob) is greater than 0.7, it is classified as a positive emotion (return value 1).
2. If the positive probability is less than 0.3, it is classified as a negative emotion (return value -1).
3. If the positive probability is between 0.3 and 0.7, it is classified as a neutral emotion (return value 0).
4. During API calls, the code pauses at intervals (sleeping) to avoid rapid request-induced data loss. If the interval is set to 1 second, there will be no loss; if set to 0.5 seconds, there will be about a 10% loss.

- Result Integrity Judgment Module Logic:

1. This module first determines which results are non-compliant;
2. It then rechecks non-compliant results to determine if they are due to "connection loss" or the input sample not meeting analysis requirements, among other errors.

## Execution Instruction
- Step-by-step guide on how to run the dashboard

## Results
- Screenshots of the dashboard
- Discussion on the price data and sentiment analysis results

## Future Work
- Potential improvements and expansions

## Conclusion
- Final thoughts on the project outcome

## Appendices
- Links to repositories, datasets, and additional resources

## Collaboration
- Details about how the team collaborated on GitHub
