# QF5214-Group_15-Project
# Stock Market Dashboard Project Report

## Executive Summary
This report presents the development process and operational details of a stock market dashboard designed to combine quantitative financial data with qualitative sentiment analysis, thereby providing investors with a holistic view of market conditions. The dashboard serves as a tool for investors to make informed decisions by examining both numerical market data and the prevailing public sentiment towards the top stocks in the market.

## Introduction

The purpose of this dashboard is to amalgamate quantitative and qualitative data streams to present a unified analysis platform for investors. By correlating financial data with public sentiment, the dashboard aims to identify potential market movements and offer insights beyond traditional financial metrics.

The tools and databases utilized for this project are as follows:

- **Quantitative Financial Data Extraction**: The price and volume data are primarily sourced from the Wind API, which provides a comprehensive array of financial data points.

- **Sentiment Analysis**: For the qualitative aspect, a Python-based web scraping program is employed to harvest commentary from two prominent investment forums, Guba and Snowball. Due to computational resource constraints, the focus is limited to the constituent stocks of the CSI 300 index.

- **Language Model for Sentiment Judgement**: Baidu's LLM (Large Language Model) is used for sentiment analysis, providing the necessary API for sentiment judgement. Despite the API's slower performance, it was selected for its no-cost advantage.

- **Data Processing (ETL)**: Python is utilized for the Extract, Transform, Load (ETL) process, ensuring that the data is adequately prepared for analysis.

- **Database Management**: The project leverages cloud-based SQL databases, allowing for efficient data storage, retrieval, and collaborative work among the team members.

- **Visualization Dashboard**: Power BI is the chosen tool for developing the final dashboard due to its robust data visualization capabilities and interactive user interface.

## Problem Statement
In the fast-paced world of stock trading, investors require real-time data that not only reflects the market trends in terms of prices and volumes but also captures the market sentiment, which often precedes market movements. The dashboard addresses this need by integrating financial data with sentiment analysis, offering a comprehensive view that supports strategic investment decisions.

## Dataset Description
The financial dataset comprises key metrics of the CSI 300 index stocks, derived from the Wind API. For sentiment analysis, public discussions related to these stocks are extracted from Guba and Snowball forums, which are then processed using Baidu's LLM to gauge the market sentiment.

## System Architecture
(To be expanded upon further discussion and technical specifics provided.)

## Implementation
(To be expanded upon further discussion and technical specifics provided.)


## Dataset Description
- Price data: Extracted from Wind API
- Sentiment data: Collected through web scraping and analyzed with a large language model

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
