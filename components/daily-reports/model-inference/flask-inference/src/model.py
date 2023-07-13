from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers

class ChatModel:
    def __init__(self):
        self.model_name = "llama-65b"
        self.tokenizer = AutoTokenizer.from_pretrained("/data/models/{}-tokenizer".format(self.model_name), device_map="auto", trust_remote_code=True, load_in_8bit=True)
        self.model = AutoModelForCausalLM.from_pretrained("/data/models/{}-model".format(self.model_name), device_map="auto", trust_remote_code=True, load_in_8bit=True)
        self.pipe = transformers.pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            trust_remote_code=True,
            device_map="auto",
            max_length=4000,
        )

    def get_reply(self, user_query):
        reply = self.pipe(user_query,
                          do_sample=True,
                          top_k=10,
                          num_return_sequences=1,
                          eos_token_id=self.tokenizer.eos_token_id,
        )
        #remove the prompt from the reply
        print(reply)
        return reply[0]['generated_text'].replace(user_query, "") 