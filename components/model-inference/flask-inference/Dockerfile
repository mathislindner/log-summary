FROM huggingface/transformers-all-latest-gpu

#RUN export https_proxy=http://lbproxy.cern.ch:8080 ; export http_proxy=http://lbproxy.cern.ch:8080 ; export no_proxy="localhost,127.0.0.1,*.cern.ch,*.local,10.0.0.0/8"

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD python3 src/app.py
#RUN pip install flask
#RUN pip install flask_cors
#RUN pip install transformers
#RUN pip install torch torchvision torchaudio
#RUN pip install einops
#RUN pip install accelerate
#RUN pip install bitsandbytes
#RUN pip install xformers