# QF5214-Group_15-Project
# Stock Market Dashboard Project Report

## Summary
This report presents the development process and operational details of a stock market dashboard designed to combine quantitative financial data with qualitative sentiment analysis, thereby providing investors with a holistic view of market conditions. The dashboard serves as a tool for investors to make informed decisions by examining both numerical market data and the prevailing public sentiment towards the top stocks in the market.

## Introduction

The purpose of the dashboard is to provide a nuanced view of the stock market by integrating quantitative financial data with sentiment analysis. This dual-faceted approach allows for a more informed analysis, as it captures the subjective sentiments of individual investors and the objective tone of financial news, both of which can significantly influence market behavior.

The development of this dashboard used the following tools and data sources:

- **Quantitative Financial Data**: Sourced from the Wind API, which offers extensive financial data for market analysis.

- **Sentiment Data**:
  - **Investor Sentiment**: Gained through Python-based web scraping of investor comments from the Guba and Snowball forums, focusing on the CSI 300 index stocks.
  - **Fund Sentiment**: Captures broader market sentiment by including commentary from the top 100 funds in China from Snowball forums, reflecting macro investor sentiment.
  - **News Sentiment**: Collected from Guba financial news publications to incorporate objective sentiment influences on the market.

- **Sentiment Analysis Model**: Utilizes Baidu's Large Language Model (LLM) API for sentiment judgement, chosen for its accessibility and cost-effectiveness despite slower processing times.

- **Data Processing and ETL**: Carried out with Python to ensure efficient data extraction, transformation, and loading into the system.

- **Database and Cloud Integration**: Managed via cloud-based SQL databases to facilitate data handling and collaboration.

- **Visualization and Dashboard Interface**: Constructed with Power BI for its dynamic data visualization capabilities, enhancing the interactive experience for users.

## Problem Statement
The modern stock market demands a sophisticated analysis tool that considers both the numerical trends and the psychological climate of the investing community. This dashboard is designed to meet that demand by merging real-time financial data with sentiment analysis, providing a comprehensive tool that anticipates market dynamics and informs investment strategies.

## Dataset Description
The financial dataset is composed of detailed metrics for the CSI 300 index stocks, courtesy of the Wind API. In parallel, the sentiment dataset is built by extracting and analyzing public discussions and financial news pertaining to these stocks and the top 100 funds in China. The sentiment data provides insights into the subjective outlook of individual investors and the objective influence of the news media on market trends.

## System Architecture
- Flow diagram of the system architecture
- Explanation of the components

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
