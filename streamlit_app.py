import streamlit as st
import os
import pandas as pd
from sentiment_analysis import fetch_news_sentiment
from data_fetcher import fetch_stock_data, fetch_top_gainers_losers
import requests

DATA_DIR = "/app/data"

# Ensure the data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Streamlit app title
st.title("Stock Data & News Sentiment Dashboard")

# Sidebar for symbol input
st.sidebar.header("Input Options")

# Multi-select dropdown for popular stock symbols
popular_symbols = ["IBM", "AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NFLX", "META", "NVDA", "ORCL"]
symbols = st.sidebar.multiselect(
    "Select Stock Symbols (or enter manually below):", 
    options=popular_symbols, 
    default=["IBM"]
)

# Text input for entering additional stock symbols manually
manual_symbols = st.sidebar.text_input("Enter Stock Symbols (comma-separated, e.g., AMD, INTC)", "")

# Combine selected symbols from dropdown and manual input
if manual_symbols:
    symbols += manual_symbols.split(',')

# Select interval for stock data
interval = st.sidebar.selectbox("Select Interval", ["1min", "5min", "15min", "30min", "60min"])

# Stock Options
st.sidebar.subheader("Stock Data Options")
stock_options = st.sidebar.multiselect("Choose options:", 
                                      ["Stock Data", "News Sentiment", "Top Gainers/Losers", "Compare Multiple Stocks"])

# Fetch stock data for multiple symbols
if "Stock Data" in stock_options:
    if st.sidebar.button("Fetch Stock Data"):
        try:
            for sym in symbols:
                stock_data = fetch_stock_data(sym.strip(), interval)
                st.subheader(f"Stock Data for {sym.strip()} ({interval})")
                st.write(stock_data)
        except ValueError as e:
            st.error(e)

# Fetch news sentiment for multiple symbols
if "News Sentiment" in stock_options:
    if st.sidebar.button("Fetch News Sentiment"):
        try:
            for sym in symbols:
                news_data = fetch_news_sentiment(sym.strip())
                st.subheader(f"News Sentiment for {sym.strip()}")
                st.write(pd.DataFrame(news_data))
        except ValueError as e:
            st.error(e)

# Fetch top gainers and losers option
if "Top Gainers/Losers" in stock_options:
    if st.sidebar.button("Fetch Top Gainers and Losers"):
        try:
            gainers, losers = fetch_top_gainers_losers()
            st.subheader("Top Gainers")
            st.write(gainers)
            st.subheader("Top Losers")
            st.write(losers)
        except ValueError as e:
            st.error(e)

# Option to compare multiple stocks
if "Compare Multiple Stocks" in stock_options:
    st.sidebar.subheader("Compare Stocks")
    compare_interval = st.sidebar.selectbox("Select Comparison Interval", ["1min", "5min", "15min", "30min", "60min"])
    
    if st.sidebar.button("Compare Stocks"):
        try:
            for sym in symbols:
                stock_data = fetch_stock_data(sym.strip(), compare_interval)
                st.subheader(f"Stock Data for {sym.strip()} ({compare_interval})")
                st.write(stock_data)
        except ValueError as e:
            st.error(e)

# Display saved data from the `/data` folder
if st.sidebar.checkbox("Show Saved Data"):
    saved_files = os.listdir(DATA_DIR)
    if saved_files:
        st.subheader("Saved Data Files:")
        for file in saved_files:
            st.write(file)
    else:
        st.write("No saved data available.")


# Input for the API to list documents
if st.button("List Documents"):
    response = requests.post("http://localhost:8000/v1/pw_list_documents")
    if response.status_code == 200:
        documents = response.json()
        st.write("Documents:")
        for doc in documents:
            st.write(f"- {doc['path']}")
    else:
        st.error("Failed to fetch documents.")

# Input for the API to answer questions
prompt = st.text_input("Enter your question:")
if st.button("Get Answer"):
    response = requests.post("http://localhost:8000/v1/pw_ai_answer", json={"prompt": prompt})
    if response.status_code == 200:
        answer = response.json()
        st.write("Answer:", answer)
    else:
        st.error("Failed to get answer.")
        
        

# import streamlit as st
# import os
# import pandas as pd
# from sentiment_analysis import fetch_news_sentiment
# from data_fetcher import fetch_stock_data, fetch_top_gainers_losers

# DATA_DIR = "./data"

# # Ensure the data directory exists
# if not os.path.exists(DATA_DIR):
#     os.makedirs(DATA_DIR)

# # Streamlit app title
# st.title("Stock Data & News Sentiment Dashboard")

# # Sidebar for symbol input
# st.sidebar.header("Input Options")
# symbols = st.sidebar.text_input("Enter Stock Symbols (comma-separated, e.g., IBM, AAPL)", "IBM, AAPL")
# interval = st.sidebar.selectbox("Select Interval", ["1min", "5min", "15min", "30min", "60min"])

# # Stock Options
# st.sidebar.subheader("Stock Data Options")
# stock_options = st.sidebar.multiselect("Choose options:", 
#                                       ["Stock Data", "News Sentiment", "Top Gainers/Losers", "Compare Multiple Stocks"])

# # Fetch stock data for multiple symbols
# if "Stock Data" in stock_options:
#     if st.sidebar.button("Fetch Stock Data"):
#         try:
#             symbol_list = symbols.split(',')
#             for sym in symbol_list:
#                 stock_data = fetch_stock_data(sym.strip(), interval)
#                 st.subheader(f"Stock Data for {sym.strip()} ({interval})")
#                 st.write(stock_data)
#         except ValueError as e:
#             st.error(e)

# # Fetch news sentiment for multiple symbols
# if "News Sentiment" in stock_options:
#     if st.sidebar.button("Fetch News Sentiment"):
#         try:
#             symbol_list = symbols.split(',')
#             for sym in symbol_list:
#                 news_data = fetch_news_sentiment(sym.strip())
#                 st.subheader(f"News Sentiment for {sym.strip()}")
#                 st.write(pd.DataFrame(news_data))
#         except ValueError as e:
#             st.error(e)

# # Fetch top gainers and losers option
# if "Top Gainers/Losers" in stock_options:
#     if st.sidebar.button("Fetch Top Gainers and Losers"):
#         try:
#             gainers, losers = fetch_top_gainers_losers()
#             st.subheader("Top Gainers")
#             st.write(gainers)
#             st.subheader("Top Losers")
#             st.write(losers)
#         except ValueError as e:
#             st.error(e)

# # Option to compare multiple stocks
# if "Compare Multiple Stocks" in stock_options:
#     st.sidebar.subheader("Compare Stocks")
#     compare_symbols = st.sidebar.text_input("Enter multiple stock symbols for comparison (comma-separated)", "AAPL, MSFT, GOOGL")
#     compare_interval = st.sidebar.selectbox("Select Comparison Interval", ["1min", "5min", "15min", "30min", "60min"])
    
#     if st.sidebar.button("Compare Stocks"):
#         try:
#             compare_symbol_list = compare_symbols.split(',')
#             for sym in compare_symbol_list:
#                 stock_data = fetch_stock_data(sym.strip(), compare_interval)
#                 st.subheader(f"Stock Data for {sym.strip()} ({compare_interval})")
#                 st.write(stock_data)
#         except ValueError as e:
#             st.error(e)

# # Display saved data from the `/data` folder
# if st.sidebar.checkbox("Show Saved Data"):
#     saved_files = os.listdir(DATA_DIR)
#     if saved_files:
#         st.subheader("Saved Data Files:")
#         for file in saved_files:
#             st.write(file)
#     else:
#         st.write("No saved data available.")


# # import streamlit as st
# # import os
# # import pandas as pd
# # from sentiment_analysis import fetch_news_sentiment
# # from data_fetcher import fetch_stock_data, fetch_top_gainers_losers

# # DATA_DIR = "./data"

# # # Streamlit app title
# # st.title("Stock Data & News Sentiment Dashboard")

# # # Sidebar for symbol input
# # st.sidebar.header("Input Options")
# # symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., IBM)", "IBM")
# # interval = st.sidebar.selectbox("Select Interval", ["1min", "5min", "15min", "30min", "60min"])

# # # Fetch stock data button
# # if st.sidebar.button("Fetch Stock Data"):
# #     try:
# #         stock_data = fetch_stock_data(symbol, interval)
# #         st.subheader(f"Stock Data for {symbol} ({interval})")
# #         st.write(stock_data)
# #     except ValueError as e:
# #         st.error(e)

# # # Fetch news sentiment button
# # if st.sidebar.button("Fetch News Sentiment"):
# #     try:
# #         news_data = fetch_news_sentiment(symbol)
# #         st.subheader(f"News Sentiment for {symbol}")
# #         st.write(pd.DataFrame(news_data))
# #     except ValueError as e:
# #         st.error(e)

# # # Fetch top gainers and losers button
# # if st.sidebar.button("Fetch Top Gainers and Losers"):
# #     try:
# #         gainers, losers = fetch_top_gainers_losers()
# #         st.subheader("Top Gainers")
# #         st.write(gainers)
# #         st.subheader("Top Losers")
# #         st.write(losers)
# #     except ValueError as e:
# #         st.error(e)

# # # Display saved data from the `/data` folder
# # if st.sidebar.checkbox("Show Saved Data"):
# #     saved_files = os.listdir(DATA_DIR)
# #     if saved_files:
# #         st.subheader("Saved Data Files:")
# #         for file in saved_files:
# #             st.write(file)
# #     else:
# #         st.write("No saved data available.")
