#dockerfile for preprocessing logs for langchain
FROM huggingface/transformers-tensorflow-gpu
WORKDIR /app
COPY . .
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pandas
RUN pip install sentence_transformers
RUN pip install transformers