FROM nvidia/cuda:11.8.0-base-ubi8
WORKDIR /app
COPY . .

RUN yum install -y python39
#install pip with yum
#RUN yum install -y python39-pip
RUN pip3 install transformers
RUN pip3 install torch torchvision torchaudio
RUN pip3 install langchain
RUN pip3 install sentence_transformers

