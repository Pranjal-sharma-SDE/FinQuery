import os
import requests
import json
import pandas as pd
from fpdf import FPDF
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Define constants
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_SENTIMENT_URL = "https://www.alphavantage.co/query"
DATA_DIR = "./data"

# Fetch news sentiment data
def fetch_news_sentiment(tickers: str, limit=50, topics=None, sort="LATEST"):
    url = f"{NEWS_SENTIMENT_URL}?function=NEWS_SENTIMENT&tickers={tickers}&apikey={ALPHA_VANTAGE_API_KEY}&limit={limit}&sort={sort}"
    if topics:
        url += f"&topics={topics}"

    response = requests.get(url)
    data = response.json()

    if "feed" in data:
        save_data(data["feed"], tickers)
        return data["feed"]
    else:
        raise ValueError("Failed to fetch news sentiment data. Check API Key or parameters.")

# Save data to JSON
def save_data(data, tickers):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    file_name = os.path.join(DATA_DIR, f"news_sentiment_{tickers.replace(',', '_')}.json")
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {file_name}")

# Extract most relevant topics (with relevance_score > threshold)
def extract_relevant_topics(feed, threshold=0.5):
    relevant_data = []
    
    for article in feed:
        # Filter relevant topics
        relevant_topics = [topic for topic in article.get('topics', []) if float(topic['relevance_score']) >= threshold]
        
        if relevant_topics:
            article_data = {
                "title": article["title"],
                "summary": article["summary"],
                "url": article["url"],
                "overall_sentiment_score": article["overall_sentiment_score"],
                "overall_sentiment_label": article["overall_sentiment_label"],
                "time_published": article.get("time_published", ""),  # Add time_published
                "topics": [topic['topic'] for topic in relevant_topics]
            }
            relevant_data.append(article_data)
    
    return relevant_data

# Save relevant data to PDF with better alignment and spacing
def save_to_pdf(relevant_data, output_file, ticker):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Add title to PDF
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"Relevant News Sentiment Summary for {ticker}", ln=True, align='C')

    # Add each article
    pdf.set_font("Arial", size=10)
    for article in relevant_data:
        pdf.ln(10)
        
        # Add article title
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=article["title"], ln=True)

        # Format and add time_published if available
        time_published = article.get("time_published", "")
        if time_published:
            try:
                # Convert time from "20240928T092400" to a readable format "YYYY-MM-DD HH:MM:SS"
                formatted_time = datetime.strptime(time_published, '%Y%m%dT%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
                pdf.set_font("Arial", 'I', 10)
                pdf.cell(200, 10, txt=f"Published on: {formatted_time}", ln=True)
            except ValueError:
                pdf.cell(200, 10, txt=f"Published on: {time_published}", ln=True)

        # Add summary
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 10, txt=f"Summary: {article['summary']}")
        
        # Add some spacing before sentiment data
        pdf.ln(3)

        # Add sentiment label and score
        pdf.cell(0, 10, txt=f"Sentiment Label: {article['overall_sentiment_label']}")
        pdf.ln(5)
        pdf.cell(0, 10, txt=f"Sentiment Score: {article['overall_sentiment_score']}")
        pdf.ln(5)

        # Add topics
        pdf.multi_cell(0, 10, txt=f"Topics: {', '.join(article['topics'])}")
        pdf.ln(5)

        # Add URL (Read more)
        pdf.set_text_color(0, 0, 255)  # Change text color for link
        pdf.cell(0, 10, txt="Read more:", link=article["url"], ln=True)
        pdf.set_text_color(0, 0, 0)  # Reset text color to black
        pdf.ln(5)

    # Output the PDF
    pdf.output(output_file)
    print(f"PDF saved to {output_file}")

# Main function to fetch, process, and save news sentiment data
def main():
    tickers = "IBM"  # Example ticker
    data = fetch_news_sentiment(tickers)
    
    # Extract relevant topics (threshold = 0.5 by default)
    relevant_data = extract_relevant_topics(data, threshold=0.5)

    # Convert relevant data to a DataFrame for further manipulation (optional)
    df = pd.DataFrame(relevant_data)
    
    # Generate unique PDF filename based on ticker
    output_pdf = os.path.join(DATA_DIR, f"relevant_news_sentiment_{tickers}.pdf")
    
    # Save the relevant data to PDF
    save_to_pdf(relevant_data, output_pdf, tickers)

if __name__ == "__main__":
    main()

