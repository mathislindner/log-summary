FROM huggingface/transformers-tensorflow-gpu
#
#WORKDIR /app
#
#COPY . .
#RUN export https_proxy=http://lbproxy.cern.ch:8080 ; export http_proxy=http://lbproxy.cern.ch:8080 ; export no_proxy="localhost,127.0.0.1,*.cern.ch,*.local,10.0.0.0/8"



#FROM python:3.9-slim
WORKDIR /app
COPY . .
#COPY requirements.txt .
#RUN pip install -r requirements.txt


#RUN pip install transformers
#RUN pip install langchain
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
#RUN pip install -i https://test.pypi.org/simple/ bitsandbytes
RUN pip install accelerate
RUN pip install xformers
#RUN pip install jq
RUN pip install einops
RUN pip install bitsandbytes

#CMD python3 src/inference.py