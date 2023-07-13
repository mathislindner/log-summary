#dockerfile for preprocessing logs for langchain
FROM huggingface/transformers-tensorflow-gpu
WORKDIR /app
COPY . .
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pandas
RUN pip install langchain
RUN pip install sentence_transformers
RUN pip install transformers
RUN pip install chromadb
#RUN pip install InstructorEmbedding
#RUN pip install torch torchvision torchaudio
#CMD python src/preprocess-logs-for-langchain.py --log_path /data/raw/logs/2023-06-28/