FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install Tesseract OCR
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Create start script to run both services
RUN echo '#!/bin/bash\nuvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run app/streamlit_app.py --server.port 8501 --server.address 0.0.0.0' > start.sh && \
    chmod +x start.sh

CMD ["./start.sh"]
