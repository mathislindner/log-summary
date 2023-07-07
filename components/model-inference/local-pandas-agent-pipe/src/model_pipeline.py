import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
def get_model_pipeline(model_name):
    model_path=f"/data/models/{model_name}-model"
    tokenizer_path=f"/data/models/{model_name}-tokenizer"

    if model_name == "open_llama_13b":
        import torch
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, device_map="auto", trust_remote_code=True, use_fast=False, torch_dtype=torch.float16)
        model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", trust_remote_code=True,torch_dtype=torch.float16)
    
    elif model_name == "llama-65b":
        model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="auto",
        load_in_8bit=True,
        max_memory= {i: '24000MB' for i in range(torch.cuda.device_count())},
        )
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, device_map="auto", trust_remote_code=True, load_in_8bit=True)
    else:
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, device_map="auto", trust_remote_code=True, load_in_8bit=True)
        model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", trust_remote_code=True, load_in_8bit=True)
        
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