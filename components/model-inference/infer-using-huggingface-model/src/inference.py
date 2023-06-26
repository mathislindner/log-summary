#pip -q install langchain huggingface_hub transformers sentence_transformers
import langchain
from langchain.document_loaders import DirectoryLoader, TextLoader, JSONLoader
from langchain.llms import HuggingFacePipeline
from langchain import PromptTemplate, LLMChain

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, AutoModelForSeq2SeqLM
import os
import argparse

def get_documents():
    alarms_json_by_receiver = os.path.join('/data', 'raw', 'alarms', 'by_receiver')
    loader = DirectoryLoader(alarms_json_by_receiver, glob='**/*.json', show_progress=True, loader_cls=JSONLoader)
    documents = loader.load()
    return documents

def get_model(model_id):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, load_in_8bit = True)
    pipe = pipeline('text2text-generation', 
                    model=model, 
                    tokenizer=tokenizer, 
                    max_length=1000)
    local_llm = HuggingFacePipeline(pipe)
    return local_llm

def get_llm_chain(prompt, llm):
    llm_chain = LLMChain(prompt, llm)
    return llm_chain

def  get_prompt():
    #mention the access to the json files
    #mention that it needs to write a short answer that summarizes the json file
    #mention that the data is about alarms that are can be caused by ...,...,...
    template = """
            {question}
            """
    prompt = PromptTemplate(template, input_variables=['question'])
    return prompt

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    #load the model
    model_id = 'facebook/blenderbot-1B-distill'
    local_llm = get_model(model_id)

    #load the documents
    documents = get_documents()
    test_doc = documents[0]

    #create the prompt for each document
    #TODO: add memory to the prompt of alarms that already have been summarized
    prompt = get_prompt()
    llm_chain = get_llm_chain(prompt, local_llm)
    alarm_receiver = 'test'
    answer = llm_chain.run(input_documents = test_doc)

    #get a summary of each document

    #save the summary of each document

