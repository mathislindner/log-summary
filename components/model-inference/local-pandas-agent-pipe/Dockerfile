FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

#RUN export https_proxy=http://lbproxy.cern.ch:8080 ; export http_proxy=http://lbproxy.cern.ch:8080 ; export no_proxy="localhost,127.0.0.1,*.cern.ch,*.local,10.0.0.0/8"

WORKDIR /app
COPY . .

RUN apt-get update
#install python 3.9 with apt-get
RUN apt-get install python3.9 -y
RUN apt-get install python3-pip -y

RUN pip3 install transformers
RUN pip3 install torch torchvision torchaudio
RUN pip3 install einops
RUN pip3 install accelerate
RUN pip3 install bitsandbytes
RUN pip3 install xformers
RUN pip3 install langchain
RUN pip3 install pandas
RUN pip3 install tabulate
RUN pip3 install scipy