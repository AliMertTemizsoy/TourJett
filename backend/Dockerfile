FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add Postgres client and bash for pg_isready
RUN apt-get update && apt-get install -y postgresql-client

COPY . .

RUN chmod +x wait-for-db.sh

CMD ["./wait-for-db.sh", "python", "run.py"]
