#dockerfile for preprocessing logs for langchain
FROM python:3.9-slim
WORKDIR /app
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD python src/preprocess-logs-for-langchain.py --log_path /data/raw/logs/2023-06-23/