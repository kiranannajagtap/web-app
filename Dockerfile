FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt requirements.txt

# Install dependencies for psycopg2
RUN apt-get update && apt-get install -y gcc libpq-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 80

CMD ["python", "app.py"]
