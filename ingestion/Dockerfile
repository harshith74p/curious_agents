FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy libs
COPY ../libs /app/libs

# Copy ingestion scripts
COPY . .

# Run multiple producers
CMD ["python", "run_all.py"] 