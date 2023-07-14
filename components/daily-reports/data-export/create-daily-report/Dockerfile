FROM python:3.8-slim
WORKDIR /app

RUN pip install pandas
RUN pip install tqdm
RUN pip install requests

COPY . .

CMD python3 src/create-daily-report.py --report_day $(date -d "yesterday" +"%d") --log_level error
