# QF5214-Group_15-Project
# Stock Market Dashboard Project Report

## Abstract
This report presents the development process and operational details of a stock market dashboard designed to combine quantitative financial data with qualitative sentiment analysis, thereby providing investors with a holistic view of market conditions. The dashboard serves as a tool for investors to make informed decisions by examining both numerical market data and the prevailing public sentiment towards the top stocks in the market.

## Problem Statement
After the Chinese stock market's steep decline in February and March, investors face a dilemma: has market sentiment bottomed out, signaling a time to buy the dip? If news headlines are overwhelmingly positive yet stock forum sentiments are bleak, it could signal an undervalued market ripe for investment. However, sifting through forums for individual comments is a time-consuming and inefficient process, and one might miss out on crucial sentiment indicators. Enter our dashboard, a fusion of real-time financial data and sentiment analysis, designed for the modern stock market. It navigates through numerical trends and investor psychology, offering a holistic view that guides investment strategies. This tool is a game-changer for investors aiming to make informed decisions in a fluctuating market.

## Introduction

The purpose of the dashboard is to provide a nuanced view of the stock market by integrating quantitative financial data with sentiment analysis. This dual-faceted approach allows for a more informed analysis, as it captures the subjective sentiments of individual investors and the objective tone of financial news, both of which can significantly influence market behavior.

The development of this dashboard used the following tools and data sources:

- **Quantitative Financial Data**: Sourced from the Wind API, which offers extensive financial data for market analysis.

- **Sentiment Data**:
  - **Investor Sentiment**: Gained through Python-based web scraping of investor comments from the Guba and Snowball forums, focusing on the CSI 300 index stocks.
  - **Fund Sentiment**: Captures broader market sentiment through Python-based web scraping of commentary from the top 100 funds in China from Guba forums, reflecting macro investor sentiment.
  - **News Sentiment**: Collected through Python-based web scraping from Guba financial news publications to incorporate objective sentiment influences on the market.

- **Sentiment Analysis Model**: Utilizes Baidu's Large Language Model (LLM) API for sentiment judgement, chosen for its accessibility and cost-effectiveness despite slower processing times.

- **Data Processing and ETL**: Carried out with Python to ensure efficient data extraction, transformation, and loading into the system.

- **Database and Cloud Integration**: Managed via cloud-based SQL databases to facilitate data handling and collaboration.

- **Visualization and Dashboard Interface**: Constructed with Power BI for its dynamic data visualization capabilities, enhancing the interactive experience for users.

## Dataset Description

The datasets for this project are multi-faceted, encompassing both financial data and sentiment data:

- **Financial Data**: Sourced from the Wind API, this dataset includes daily stock prices, trading volumes, and holder information. Key financial metrics, such as stock returns, are computed to establish a foundation for quantitative analysis. Additionally, we obtain detailed stock information, including the `industries` stocks belong to and `hot concepts` they are associated with. This information serves as vital dimensions for subsequent data aggregation and analysis.
  
- **Sentiment Data**: Extracted using Python web scrapers, this includes investor comments from Guba and Snowball, and news content related to stocks and funds. The sentiment is analyzed for positive or negative emotions using Baidu's LLM.

- **Metrics Definition**: Metrics are defined by a combination of time periods (e.g., last 1 day, last 7 days), entities (stocks, funds), and data types (return, comment, emotion). Derived metrics are created based on these definitions, such as 'last 7 days stock positive number comment' indicating the count of positive comments over the past week.

## Data Architecture and Data Pipeline

The stock market dashboard relies on a robust data architecture and pipeline designed for efficient data flow from source to presentation. The architecture is structured into several key layers, each serving a pivotal role in the processing and analysis of data.

### Data Sources
The foundation of our dashboard is built upon data acquired from diverse sources:
- **Wind API**: Provides a wealth of financial data points, including stock information and trading activities.
- **Web Crawlers**: These are utilized to gather sentiment data from various financial websites, capturing the mood and opinions of the market participants.

### ODS
This layer serves as the staging area for raw data:
- It contains tables for the initial storage of stock information , stock market data and sentiment data (`ods_comment_ef_stock`, `ods_comment_sb_stock`, `ods_news_ef_stock`, `ods_comment_ef_fund`).


### DWD and DIM
After the data is collected, it goes through an ETL process and is loaded into our Data Warehouse, which has two components:
- **DWD**: Stores the detailed, atomic-level data.
  - **Price and Volume Domain**: Here, we maintain the granularity at the daily level for each stock. The `dwd_market_price_di` fact table stores this daily price and volume information, providing a detailed view of market activities.
  - **Sentiment Domain**: This domain differentiates between stocks and funds to provide a focused view of market sentiment. 
    - Fact tables for sentiment are dedicated to stock sentiment (`dwd_stock_sentiment_di`) and fund sentiment (`dwd_fund_sentiment_di`), where each record corresponds to sentiment data for individual stocks and funds, respectively.
    - Sentiment cleansing and emotion tagging are critical processes completed in this layer. We standardize and clean the sentiment data from various sources before applying Baidu's LLM for emotion analysis, resulting in sentiment tags that classify data as positive, negative, or neutral. This enrichment allows for sophisticated sentiment-based insights into market trends.

- **DIM**: Includes dimension tables such as `dim_stock_info` and `dim_date_info`, which are used to add context to the facts through attributes like dates, stock indices, and industry sectors.

### DWS
This layer facilitates business intelligence and analysis:
- It includes tables that have been specifically designed based on business requirements, such as `dws_stock_price_performance_1d` for daily stock performance and `dws_stock_sentiment_analysz_1d` for sentiment analysis.


### ADS
The ADS is where the curated data for final presentation is stored:
- This includes tables like `ads_stock_ind_return_comment_1d` and `ads_stock_ind_comment_timent_share_1d`. These are constructed to feed customized metrics directly into the dashboard.

### Data Pipeline
The process through which data is transformed from raw form into actionable insights involves several stages:
1. **Extraction**: Initially, data is extracted from the Wind API and web sources through our crawlers.
2. **Transformation**: The raw data is then transformed, where it is cleaned, normalized, and enriched to fit into our dwd.
3. **Loading**: The transformed data is subsequently loaded into the respective DWD and DIM tables for detailed analysis and context.
4. **Processing**: Data in DWS undergoes further aggregation and analysis to construct business-centric views.
5. **Presentation**: Finally, the data is presented through the dashboard, which provides a visual and interactive means for users to explore market insights.

## Implementation
- Code snippets and explanations of key functions
- Details on the API integration and web scraping process
- Description of the sentiment analysis model

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
