import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
def get_model_pipeline(model_name):
    if model_name == "open_llama_13b":
        import torch
        tokenizer = AutoTokenizer.from_pretrained(f"/data/models/{model_name}-tokenizer", device_map="auto", trust_remote_code=True, use_fast=False, torch_dtype=torch.float16)
        model = AutoModelForCausalLM.from_pretrained(f"/data/models/{model_name}-model", device_map="auto", trust_remote_code=True,torch_dtype=torch.float16)
    else:
        tokenizer = AutoTokenizer.from_pretrained(f"/data/models/{model_name}-tokenizer", device_map="auto", trust_remote_code=True, load_in_8bit=True)
        model = AutoModelForCausalLM.from_pretrained(f"/data/models/{model_name}-model", device_map="auto", trust_remote_code=True, load_in_8bit=True)
    ############################################################################################################
    #https://betterprogramming.pub/creating-my-first-ai-agent-with-vicuna-and-langchain-376ed77160e3
    ############################################################################################################
    #"text-generation",
    pipe = transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        trust_remote_code=True,
        do_sample = True,
        max_length=2048,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
    )
    return pipe