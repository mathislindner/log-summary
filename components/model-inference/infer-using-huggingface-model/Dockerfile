FROM huggingface/transformers-pytorch-gpu:latest
#
#WORKDIR /app
#
#COPY . .
#RUN export https_proxy=http://lbproxy.cern.ch:8080 ; export http_proxy=http://lbproxy.cern.ch:8080 ; export no_proxy="localhost,127.0.0.1,*.cern.ch,*.local,10.0.0.0/8"
#RUN apt-get install kmod -y
#
#CMD rmmod nvidia_uvm
#CMD modprobe nvidia_uvm
#CMD python src/inference.py


#FROM python:3.9-slim
WORKDIR /app
COPY . .
#COPY requirements.txt .
RUN pip install -r requirements.txt


##RUN pip install transformers
#RUN pip install langchain
##RUN pip install torch torchvision torchaudio
#RUN pip install -i https://test.pypi.org/simple/ bitsandbytes
#RUN pip install accelerate
#RUN pip install xformers
#RUN pip install jq

#CMD python3 src/inference.py