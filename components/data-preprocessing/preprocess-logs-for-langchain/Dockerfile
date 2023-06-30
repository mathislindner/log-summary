#dockerfile for preprocessing logs for langchain
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD python src/preprocess-logs-for-langchain.py --log_path /data/raw/logs/2023-06-28/