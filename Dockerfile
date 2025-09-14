# Use official Python slim image
FROM python:3.11-slim

# Install Tesseract OCR
RUN apt-get update && apt-get install -y tesseract-ocr

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r webapp/requirements.txt
RUN pip install -r requirements.txt

# Expose port (default Flask port)
EXPOSE 5000

# Run the Flask app
CMD gunicorn --workers=1 --bind=0.0.0.0:${PORT} webapp.app:app
