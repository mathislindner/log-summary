#use a langchain agent to trasverse the df of the logs to answer questions
# for example: what happened to the host "" in the last 15 minutes?
# retrieves the logs of the host in the last 15 minutes
# summarize the logs
# return the summary...

from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
from langchain.agents import create_pandas_dataframe_agent
import pandas as pd

model_name = "tiiuae/falcon-40b-instruct"

tokenizer = AutoTokenizer.from_pretrained("/data/models/falcon-40b-instruct-tokenizer", device_map="auto", trust_remote_code=True, load_in_8bit=True)
model = AutoModelForCausalLM.from_pretrained("/data/models/falcon-40b-instruct-model", device_map="auto", trust_remote_code=True, load_in_8bit=True)

pipe = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    trust_remote_code=True,
    device_map="auto",
)

df_errors= pd.read_csv("/data/preprocessed/logs/2023-06-28/error.csv")
df_warnings= pd.read_csv("/data/preprocessed/logs/2023-06-28/warning.csv")

agent = create_pandas_dataframe_agent(pipe, [df_errors, df_warnings])