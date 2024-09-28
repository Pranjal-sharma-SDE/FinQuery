FROM pathwaycom/pathway:latest

WORKDIR /app

RUN apt-get update \
    && apt-get install -y python3-opencv tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

COPY requirements.txt ./
RUN pip install -U --no-cache-dir -r requirements.txt

COPY . .

# Expose the ports for both the backend and Streamlit
EXPOSE 8000
EXPOSE 8501

# Run both the backend and Streamlit app
CMD ["sh", "-c", "python app.py & streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0"]