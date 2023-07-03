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
RUN pip3 install pandas
RUN pip3 install einops
RUN pip3 install accelerate
RUN pip3 install bitsandbytes
RUN pip3 install tabulate
RUN pip3 install xformers

