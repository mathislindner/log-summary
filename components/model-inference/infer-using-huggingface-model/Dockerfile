FROM python:3.9-slim
WORKDIR /app

#COPY requirements.txt .
COPY . .

RUN pip install transformers
RUN pip install langchain
RUN pip install torch torchvision torchaudio
RUN pip install -i https://test.pypi.org/simple/ bitsandbytes
RUN pip install accelerate

CMD python src/inference.py