# FinQuery - Finance News & Stock Data RAG App

FinQuery is a finance-focused Retrieval-Augmented Generation (RAG) application that provides real-time stock market data, news sentiment analysis, and top gainers/losers insights. Built using the Pathway framework, Alpha Vantage API, and Streamlit for the interface, it offers interactive financial information retrieval with visualization and document generation.

![FinQuery Infographic](https://res.cloudinary.com/dqhyudo4x/image/upload/v1727539537/img_kqeea6.jpg)

![Logo](https://res.cloudinary.com/dqhyudo4x/image/upload/v1727527200/Gemini_Generated_Image_9gcau79gcau79gca_utq1rr.jpg)

![ FinQuery](https://res.cloudinary.com/dqhyudo4x/image/upload/v1727539536/Final_finquery_se74ka.jpg)

## Features

- **Stock Data Fetching**: Retrieve real-time stock prices and time series data for multiple symbols.
- **News Sentiment Analysis**: Fetch and analyze sentiment for relevant financial news based on stock tickers.
- **Top Gainers/Losers**: Identify top-performing and least-performing stocks in the market.
- **PDF Generation**: Generate and download PDF reports of news sentiment analysis.
- **Multi-Symbol Comparison**: Compare stock data across multiple time intervals.

---

## Tech Stack

- **Backend**: Python, Pathway (RAG with LLM integration)
- **Frontend**: Streamlit (Interactive web interface)
- **APIs**: Alpha Vantage (Stock data, news sentiment)
- **Libraries**: Pandas, Requests, FPDF, YAML, Dotenv
- **Containerization**: Docker

---

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Docker (for containerization)
- Alpha Vantage API Key (You can [get it here](https://www.alphavantage.co/support/#api-key))

### Clone the Repository

```bash
git clone https://github.com/Pranjal-sharma-SDE/FinQuery.git
cd FinQuery
```

### Set Up Environment

1. Set up environment variables:
   - Create a `.env` file in the root directory with the following contents:
     ```env
     ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
     GEMINI_API_KEY=*******
     ```


---

## Usage


### Docker Deployment

1. **Build the Docker image**:
   ```bash
   docker build -t finquery-app .
   ```

2. **Run the Docker container**:
   ```bash
   docker run -p 8000:8000 -p 8501:8501 -v "${PWD}/data:/app/data" finquery
   ```

3. **Access the app**:
   - Navigate to `http://localhost:8501`.

---

## Configuration

You can configure various options in the `config.yaml` file:

```yaml
llm_config:
  model: "gemini/gemini-pro"
host_config:
  host: "0.0.0.0"
  port: 8000
cache_options:
  with_cache: True
  cache_folder: "./Cache"
sources:
  - local_files:
    kind: local
    config:
    path: "/data"
```

## 

![FinQuery](https://res.cloudinary.com/dqhyudo4x/image/upload/v1727541266/ezgif-3-498ec7a521_eylnuw.gif)

---

## Features and Functionalities

1. **Stock Data**:
   - Fetch stock data for symbols like IBM, AAPL, MSFT, etc.
   - Adjustable time intervals (1min, 5min, 15min, 60min).

   ![Fetch Timeseries data](https://res.cloudinary.com/dqhyudo4x/image/upload/v1727539537/Timeserires_frc6ul.jpg)

2. **News Sentiment Analysis**:
   - Pull recent news articles based on stock symbols.
   - Extract relevant topics, sentiment scores, and labels.
   - Generate PDF reports with detailed sentiment analysis.
   - Download and view PDF reports.
   - Questions Answerable.

   ![News Sentiment Analysis](https://res.cloudinary.com/dqhyudo4x/image/upload/v1727539537/Pdf_view_imphoy.jpg)

   ![News Sentiment Analysis](https://res.cloudinary.com/dqhyudo4x/image/upload/v1727539536/Final_finquery_se74ka.jpg)

3. **Top Gainers/Losers**:
   - Display top-performing stocks based on real-time data.

   ![Top Gainers/Losers](https://res.cloudinary.com/dqhyudo4x/image/upload/v1727539537/Top_gainers_yv2diz.jpg)

   ![Top Losers](https://res.cloudinary.com/dqhyudo4x/image/upload/v1727539537/top_loss_loxaux.jpg)

4. **Comparison of Multiple Stocks**:
   - Compare stock performance across different time intervals.

---

## File Structure

```
.
├── app.py                     # Main backend logic using Pathway RAG
├── data/                      # Data files stored in this folder
├── data_fetcher.py            # Fetch stock data and top gainers/losers
├── sentiment_analysis.py      # News sentiment analysis and PDF generation
├── streamlit_app.py           # Streamlit front-end code
├── config.yaml                # Configuration file for models and data sources
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker setup
└── .env                       # Environment variables for API keys
```

---

## Future Enhancements

- **User Authentication**: Implement secure logins for personalized data retrieval.
- **Historical Data Analysis**: Include features for analyzing historical stock trends.
- **Portfolio Management**: Allow users to track their portfolio and gain insights.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author

Developed by Pranjal Sharma, with contributions in finance, data science, and backend development.

Feel free to connect on [LinkedIn](https://www.linkedin.com/in/pranjal-sharma-93b4a01a4/) or email me at yourname@example.com for further queries.

---

## Acknowledgements

- Thanks to **Pathway** for the RAG framework and **Alpha Vantage** for providing the stock and sentiment data.

---
