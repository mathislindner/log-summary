import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.chains import LLMChain
#from langchain.agents import create_pandas_dataframe_agent
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
    max_length=1600,
)

llm = HuggingFacePipeline(model_id = model_name, pipeline = pipe)

df_errors= pd.read_csv("/data/preprocessed/logs/2023-06-28/error.csv")
df_warnings= pd.read_csv("/data/preprocessed/logs/2023-06-28/warning.csv")

agent = create_pandas_dataframe_agent(llm, [df_errors, df_warnings], verbose=True)
print(agent.run("get me one random error"))