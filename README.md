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

- **Financial Data**: Sourced from the Wind API, this dataset includes daily stock prices, trading volumes, and holder information. Key financial metrics, such as stock returns, are computed to establish a foundation for quantitative analysis. Additionally, we obtain detailed stock information, including the industries stocks belong to and hot concepts they are associated with. This information serves as vital dimensions for subsequent data aggregation and analysis.
  
- **Sentiment Data**: Extracted using Python web scrapers, this includes investor comments from Guba and Snowball, and news content related to stocks and funds. The sentiment is analyzed for positive or negative emotions using Baidu's LLM.

- **Metrics Definition**: Metrics are defined by a combination of time periods (e.g., last 1 day, last 7 days), entities (stocks, funds), and data types (return, comment, emotion). Derived metrics are created based on these definitions, such as 'last 7 days stock positive number comment' indicating the count of positive comments over the past week.

## System Architecture

The system architecture is divided into several layers, each with a specific role in the processing and storage of data:

- **Source Data**: This is the initial data ingestion layer where financial data is sourced from the Wind API and sentiment data is gathered from online forums and news sites through web crawlers.

- **Operational Data Store (ODS)**: The raw data is stored here immediately after extraction. It includes tables for stock information, stock price, stock holder data, and various types of comments and news related to stocks and funds.

- **Data Warehouse (DWD/DIM)**: After the ETL processes, data is transformed into a dimensional model. This includes detailed dimension tables like `dim_stock_info` and `dim_date_info` and fact tables such as `dwd_market_price_di` for market prices and `dwd_stock_sentiment_di` for stock sentiment.

- **Data Warehouse Service (DWS)**: This layer contains transformed and aggregated data, structured based on business requirements for querying and analysis. It includes tables like `dws_stock_price_performance_1d` and `dws_stock_sentiment_analysz_1d`.

- **Analytical Data Store (ADS)**: The ADS will store customized metric data for services and displays on the dashboard. (To be designed and detailed.)

- **Analysis & Presentation**: The final layer is where the processed and stored data is analyzed and presented in a graphical user interface, such as the Power BI dashboard.

...

(Additional sections to continue after this.)


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
