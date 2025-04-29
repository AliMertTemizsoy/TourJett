FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add Postgres client and bash for pg_isready
RUN apt-get update && apt-get install -y postgresql-client

# Copy the wait-for-db.sh script FIRST
COPY wait-for-db.sh .
RUN chmod +x wait-for-db.sh

# Then copy the rest of the application
COPY . .

CMD ["./wait-for-db.sh", "python", "run.py"]