#dockerfile for preprocessing alarms for langchain

FROM python:3.8-slim
WORKDIR /app

#COPY requirements.txt .

#RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu120
#RUN pip install langchain


COPY . .

CMD python src/preprocess-alarms-for-langchain.py

