#dockerfile for preprocessing alarms for langchain

FROM python:3.8-slim
WORKDIR /app

#COPY requirements.txt .

#RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python src/preprocess-alarms-for-langchain.py

