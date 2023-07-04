import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
#from langchain.agents import create_pandas_dataframe_agent
import pandas as pd

#model_id = "tiiuae/falcon-40b"
#model_name = "falcon-40b-instruct"
model_name = "falcon-40b"
tokenizer = AutoTokenizer.from_pretrained("/data/models/{model_name}-tokenizer", device_map="auto", trust_remote_code=True, load_in_8bit=True)
model = AutoModelForCausalLM.from_pretrained("/data/models/{model_name}-model", device_map="auto", trust_remote_code=True, load_in_8bit=True)

pipe = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    trust_remote_code=True,
    device_map="auto",
    max_length=500,
)

llm = HuggingFacePipeline(model_id = model_name, pipeline = pipe)

df_errors= pd.read_csv("/data/preprocessed/logs/2023-06-28/error.csv")
df_warnings= pd.read_csv("/data/preprocessed/logs/2023-06-28/warning.csv")

#agent = create_pandas_dataframe_agent(llm, [df_errors, df_warnings], verbose=True)
#print(agent.run("get me one random error"))

#first chain to translate english to a pandas query
pandas_template = PromptTemplate(input_variables=["df_name","df","question"],
                         template="""
                         ###INSTRUCTIONS###
                         You are given a pandas dataframe called {df_name}.
                         The columns of the dataframe are: {df.columns}.
                         Your goal is to create a pandas query for the dataframe to answer a Question.
                         You are only allowed to reply with a pandas query.
                         Do not explain your answer. Very important: Do not say anything else! just write the pandas query.
                         ###QUESTION###
                         {question}.
                         ###PANDAS QUERY###
                         """
                        )

chain_get_pandas_query = LLMChain(llm = llm, prompt = pandas_template, verbose = True)
query = chain_get_pandas_query.run({"df_name": "df_errors", "question": "how many errors are there?"})
print(query)

#convert the string query to a pandas query
df = exec(query)