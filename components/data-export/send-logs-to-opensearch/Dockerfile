FROM python:3.8-slim
WORKDIR /app

RUN pip install opensearch-py
RUN pip install pandas
RUN pip install tqdm

COPY . .

#CMD python3 src/send-logs-to-opensearch.py 