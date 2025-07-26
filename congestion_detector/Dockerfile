FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY congestion_detector/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared libraries
COPY libs/ ./libs/

# Copy agent code
COPY congestion_detector/ .

# Copy sample data for training
COPY sample_data/ ./sample_data/

# Set environment variables
ENV PYTHONPATH=/app

# Run the agent using Google ADK
CMD ["python", "agent.py"] 