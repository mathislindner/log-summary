import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.agents import create_pandas_dataframe_agent
import pandas as pd

#model_id = "tiiuae/falcon-40b"
#model_name = "falcon-40b-instruct"
model_name = "falcon-40b"
#model_name = "xgen-7b-8k-base"

tokenizer = AutoTokenizer.from_pretrained(f"/data/models/{model_name}-tokenizer", device_map="auto", trust_remote_code=True, load_in_8bit=True)
model = AutoModelForCausalLM.from_pretrained(f"/data/models/{model_name}-model", device_map="auto", trust_remote_code=True,  load_in_8bit=True, temperature=0)
############################################################################################################
#https://betterprogramming.pub/creating-my-first-ai-agent-with-vicuna-and-langchain-376ed77160e3
############################################################################################################

pipe = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    trust_remote_code=True,
    do_sample = True,
    max_length=1500,
    top_k=30,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.eos_token_id,
)
#return_full_text = False,

llm = HuggingFacePipeline(model_id = model_name, pipeline = pipe)

df_errors= pd.read_csv("/data/preprocessed/logs/2023-06-28/error.csv")
#df_warnings= pd.read_csv("/data/preprocessed/logs/2023-06-28/warning.csv")

agent = create_pandas_dataframe_agent(llm, df_errors, verbose=True)
answer = agent.run("when you are using the python tool, do not assign to another variable. You should directly execute the print of the full command. Which host wrote the last message according to the timestamp?")
print("answer:", answer)
"""
from langchain.agents import load_tools

agent = initialize_agent(tools,
                             llm,
                             agent="chat-zero-shot-react-description",
                             verbose=True)
"""
#
##first chain to translate english to a pandas query
#pandas_template = PromptTemplate(
#    input_variables=["df_name","df_columns","question"],
#    template="<INSTRUCTIONS>You are given a pandas dataframe called {df_name}. The columns of the dataframe are: {df_columns}.Your goal is to create a pandas query for the dataframe to answer a Question. You are only allowed to reply with a pandas query. Do NOT explain your answer. Delimit the query with a tag QUERY.<\INSTRUCTIONS>\n<QUESTION>{question}<\QUESTION>",
#    )
#
#chain_get_pandas_query = LLMChain(llm = llm, prompt = pandas_template, verbose = True)
#answer = chain_get_pandas_query.run({"df_name": "df_errors","df_columns": str(df_errors.columns), "question": "which host wrote the most amount of errors?"})
#print("answer:", answer)
##only use what is between the answer tags <ANSWER></ANSWER>
##select first sentence
#first_line = answer.splitlines()[1]
#query = first_line.split("<ANSWER>")[1].split("<\\ANSWER>")[0]
#print("query:", query)
#
##convert the string query to a pandas query
##TODO:this is very unsafe, easy to inject code
#result = None
#exec('result = ' + query)
#print(result)
#
#############################################################################################################
#
##second chain to explain the queries answer
##answer can be an integer, string or pandas dataframe
#if type(result) is int or type(result) is str:
#    str_int_template = PromptTemplate(
#        input_variables=["answer","question"],
#        template="<INSTRUCTIONS>You are given a question where the answer has been found to be an integer or a string Your goal is to answer the Question in a friendly way using the answer. The task is about retranscribing the answer in a nicer way to answer the question. Delimit the query with a tag <MESSAGE> <\INSTRUCTIONS>\n<QUESTION>{question}<\QUESTION>\n<ANSWER>{answer}<\ANSWER>",
#        )
#    chain_explain_answer = LLMChain(llm = llm, prompt = str_int_template, verbose = True)
#    message = chain_explain_answer.run({"answer": str(result), "question": "how many errors are there?"})
#
#elif type(result) is pd.DataFrame:
#    #if the dataframe is small enoguh
#    print("answer:", answer)