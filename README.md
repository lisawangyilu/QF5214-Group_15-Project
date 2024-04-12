# QF5214-Group_15-Project
# Stock Market Dashboard Project Report

## Abstract
This report presents the development process and operational details of a stock market dashboard designed to combine quantitative financial data with qualitative sentiment analysis, thereby providing investors with a holistic view of market conditions. The dashboard serves as a tool for investors to make informed decisions by examining both numerical market data and the prevailing public sentiment towards the top stocks in the market.

## Problem Statement
After the Chinese stock market's steep decline in February and March, investors face a dilemma: has market sentiment bottomed out, signaling a time to buy the dip? If news headlines are overwhelmingly positive yet stock forum sentiments are bleak, it could signal an undervalued market ripe for investment. However, sifting through forums for individual comments is a time-consuming and inefficient process, and one might miss out on crucial sentiment indicators. Enter our dashboard, a fusion of real-time financial data and sentiment analysis, designed for the modern stock market. It navigates through numerical trends and investor psychology, offering a holistic view that guides investment strategies. This tool is a game-changer for investors aiming to make informed decisions in a fluctuating market!

## Introduction

The purpose of the dashboard is to provide a nuanced view of the stock market by integrating quantitative financial data with sentiment analysis. 

The development of this dashboard used the following tools and data sources:

- **Quantitative Financial Data**: Sourced from the Wind API, which offers extensive financial data for market analysis.

- **Sentiment Data**:
  Gained through Python-based web scraping
  - **Investor Sentiment**: Gained investor comments from the Guba and Snowball forums, focusing on the CSI 300 index stocks.
  - **Fund Sentiment**: Captures broader market sentiment commentary from the top 100 funds in China reflecting macro investor sentiment.
  - **News Sentiment**: Collected from Guba financial news publications to incorporate objective sentiment influences on the market.

- **Sentiment Analysis Model**: Utilizes Baidu's Large Language Model (LLM) API for sentiment judgement, chosen for its accessibility and cost-effectiveness despite slower processing times.

- **Data Processing and ETL**: Carried out with Python to ensure efficient data extraction, transformation, and loading into the system.

- **Database and Cloud Integration**: Managed via Alibaba-cloud-based SQL databases to facilitate data handling and collaboration.

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

- **DIM**: Includes dimension tables such as `dim_stock_info` , `dim_date_info` and `dim_date_info`, which are used to add context to the facts through attributes like dates, stock indices, and industry sectors.

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

This section outlines the technical implementation of our stock market dashboard, focusing on data collection and sentiment analysis.

### Web Crawling Sources

We utilized two primary sources for web scraping:

- **Xueqiu**: A leading Chinese financial platform that provides market data and investor insights.
  - Source: [Xueqiu](https://xueqiu.com/)
- **Eastmoney Guba**: A forum where users discuss stocks, mutual funds, and financial news.
  - Source: [Eastmoney Guba](https://guba.eastmoney.com/)

### Advanced Web Scraping Techniques

To collect data from Xueqiu and Eastmoney Guba, we designed sophisticated crawlers employing Python libraries like `requests`, `json`, `lxml`, `pandas`, `re`, and `pymysql`. Our scraping strategy included the following techniques to overcome anti-scraping measures:

1. **Local Proxy Pool Technique**:
   - We used a local proxy pool to prevent IP blocking, managed by the ProxyPool library, which ensures a supply of functional proxies.
   - Library: [ProxyPool](https://github.com/Python3WebSpider/ProxyPool?tab=readme-ov-file)

2. **Random User-Agent Header**:
   - A variety of user-agent strings are used to mimic genuine user behavior and reduce the risk of detection.

3. **Time Delay and Implicit Waits**:
   - To simulate human-like activity, we introduced random time intervals between requests and employed implicit waits for dynamic content loading.

### Spark and Scheduling Logic

We automated the execution of multiple spider programs through scheduling. The daily-collected data is processed using Spark for MapReduce operations and stored in databases categorized by source. We utilized `spark.py` for data processing and `CrawlerScheduler.py` for task scheduling, ensuring efficient and regular data updates.

### API Integration and Sentiment Analysis Process

#### Baidu AI API Usage Instructions

- Required Credentials: We used the APP_ID, API_KEY, and SECRET_KEY to authenticate with Baidu's sentiment analysis service.
- AI NLP Client: With the credentials, we instantiated `AipNlp` to analyze text sentiment.

#### Sentiment Analysis Model Description

The model includes:

- A sentiment analysis model classifies text as positive (return 1) if the positivity probability is above 0.7, negative (return -1) if below 0.3, and neutral (return 0) if between 0.3 and 0.7.
- A result integrity judgment module to verify analysis outcomes and handle non-compliant results.

### Data Retrieval and Processing

We extracted comments related to specific funds, applied sentiment analysis using Baidu AI Cloud API, and processed the data through various steps:

1. **Preliminary Inspection**: Quick review of the dataset's head and tail for an initial understanding.
2. **Data Sorting**: Organizing data by the `update_time` and other dimension fields for chronological consistency.
3. **Timestamp Addition**: Injecting a `input_date_time` field to log the ingestion time into our system.

### Data Aggregation

Our data aggregation process emphasizes consistency and scalability, requiring field standardization and ongoing evaluation to ensure compatibility as the dataset grows.

## Results

The analysis of market sentiment data collected from web scraping and the Wind API covers a broad range of indicators, from news, reviews, to stock prices, focusing on the period from March 1st to March 31st, 2024. Below are the key findings from our visualizations:

### Sentiment Analysis in Different Media

- **News vs. Comments Sentiment**: News items tend to show a higher positive sentiment compared to comments. Specifically, stock news had a 71.2% positivity rate, while stock comments and fund comments showed a 54.4% and 50.8% negativity rate, respectively.

### Correlation between Media Coverage and Stock Prices

- **Coverage vs. Stock Prices**: The volume of comments and reviews increased throughout the month, regardless of fluctuations in stock prices. Notably, media coverage was more extensive on weekdays and reduced over weekends, indicating no clear correlation between coverage volume and stock price movements.

### Sentiment and Stock Return Correlation

- **Sentiment and Return**: There appears to be a correlation between market sentiment and stock returns. Positive sentiment increases with higher positive returns and vice versa. For instance, in return intervals exceeding 8%, positive and negative sentiments accounted for 28.79% and 51.65%, respectively. Conversely, in intervals below -8%, these figures were 21.15% and 58.54%.

### Media Engagement by Platform

- **Engagement Rates across Platforms**: EastFund had the highest post volume but the lowest engagement in terms of readings and comments per post. In contrast, SnowBall had fewer posts but significantly higher average readings per post.

### Sectorial Coverage Concentration

- **Industry-Specific Coverage**:
  - Stock and fund comments showed significant concentration in certain industries. For stocks, Information Technology, Financials, and Industries were the focus, while fund comments concentrated on Energy, Financials, and Industries.
  - A polarization phenomenon was observed in sectors with declining stock prices—some sectors had very concentrated media coverage while others had sparse coverage.

### Coverage of Hot Concepts

- **Popular Concepts in Coverage**: Both stocks and funds covered several key concepts extensively, including Baijiu, Photovoltaics, New Energy, Semiconductors, and Artificial Intelligence. The coverage shows substantial overlap in the concepts highlighted by both stocks and funds, reflecting a common interest area across different types of investments.

These findings illustrate the diverse dynamics of market sentiment and its interaction with media coverage and industry focus. The data not only enhances our understanding of market behavior but also assists investors in making informed decisions based on underlying sentiment trends.


## Future Work

In considering the future trajectory of our stock market dashboard project, we have identified several avenues for enhancement and expansion:

### Cloud Infrastructure Migration

With additional funding, we can migrate our entire operation to the cloud. This move will not only facilitate scalability but also improve reliability and performance.
- **Automated Daily Data Updates**: Integrating scheduled tasks on the cloud will enable us to perform daily data refreshes seamlessly, ensuring our dashboard reflects the most up-to-date information.
- **Optimizing Spark’s Distributed Computing Power**: By running our Spark-based processing in the cloud, we can take full advantage of the cloud’s elasticity and scalability. This means our Spark jobs can dynamically allocate more resources during high demand and scale down during quieter periods, optimizing cost and performance.

### User Experience Optimization

- **Interactive Features**: Adding more interactive elements, such as customizable charts and user-driven queries, can significantly enhance user engagement and satisfaction.

## Conclusion

Our project has successfully delivered a robust and scalable stock market dashboard powered by a well-architected data workflow. We’ve navigated anti-scraping challenges, accelerated our data processes with Spark, and brought insights to life through Power BI. These achievements reflect our dedication to creating a dynamic tool for investors. Looking ahead, we're poised to enhance our system's capabilities, with cloud deployment and further optimizations on the horizon, ensuring our dashboard remains a pivotal resource in the evolving world of financial analytics.

## Appendices
- [Links to repositories](https://github.com/lisawangyilu/QF5214-Group_15-Project)
- 4-tier datasets all in Alibaba-cloud-based SQL databases 'mysql+pymysql://user:password@***********:3306/qf5214'  
- **Access Note**:
Please be aware that due to network fluctuations, the connection port may occasionally be unstable. If you experience issues connecting to the database, consider attempting access during a different time of day.


## Collaboration

Our team's collaboration was orchestrated via GitHub. The project was compartmentalized into distinct segments, each managed by team members with specialized expertise:

- **Data Architecture**: Wei Qi
- **Wind API Integration**: Wei Qi
- **Web Crawling**: Zhou Zijian, Xu Jiacheng, Zhong Minghao and Wang Wujie
- **Data Cleaning and Sentiment Analysis**: Wang Wujie, Zhou Zijian, Xu Jiacheng, Zhong Minghao, Bai Feifan, Wang Yilu and Peng Yuezhi
- **ETL Process Management**: Peng Yuezhi, Bai Feifan and Wang Yilu
- **Dashboard Implementation**: Wang Yilu
- **Report Compilation**: Wei Qi
- **Presentation Preparation**: Bai Feifan.

Each segment involved rigorous peer reviews and iterative enhancements, supported by GitHub's issue tracking, pull requests, and continuous integration tools to maintain high code quality and project alignment.

