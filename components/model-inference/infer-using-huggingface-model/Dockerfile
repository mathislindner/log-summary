FROM huggingface/transformers-tensorflow-gpu

#RUN export https_proxy=http://lbproxy.cern.ch:8080 ; export http_proxy=http://lbproxy.cern.ch:8080 ; export no_proxy="localhost,127.0.0.1,*.cern.ch,*.local,10.0.0.0/8"

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt