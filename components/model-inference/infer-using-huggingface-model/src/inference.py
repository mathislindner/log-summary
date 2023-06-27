#langchain imports
import langchain
from langchain.document_loaders import DirectoryLoader, TextLoader, JSONLoader
from langchain.llms import HuggingFacePipeline
from langchain import PromptTemplate, LLMChain
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, AutoModelForSeq2SeqLM
#regular imports
import os
import argparse

def get_documents():
    alarms_json_by_receiver = os.path.join('/data', 'raw', 'alarms', 'by_receiver')
    loader = DirectoryLoader(alarms_json_by_receiver, glob='**/*.json', show_progress=True, loader_cls=JSONLoader)
    documents = loader.load()
    return documents

def get_model(model_id):
    device = "cuda:0"
    tokenizer = AutoTokenizer.from_pretrained(model_id).to(device)
    model = AutoModelForCausalLM.from_pretrained(model_id).to(device)
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
            based on this json document, summarize the issue that caused the alarm in bullet points.
            """
    prompt = PromptTemplate(template, input_variables=[])
    return prompt

def summarize_document(document, llm_chain):
    return llm_chain.run(input_documents = document)


if __name__ == '__main__':
    import torch
    print(torch._C._cuda_getDeviceCount())
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
    answers = []
    for document in documents:
        answers.append(summarize_document(document, llm_chain))
    print(answers)

