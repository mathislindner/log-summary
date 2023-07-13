from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, AutoModelForSeq2SeqLM

model_id = 'google/flan-t5-xxl'
tokenizer = AutoTokenizer.from_pretrained(model_id, max_length=512)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id, max_length=512, load_in_8bit=True)

pipe = pipeline(
    "text2text-generation",
    model=model, 
    tokenizer=tokenizer, 
    max_length=512,

)

query="""
INSTRUCTION: Answer the following question with a full sentence: Which server is responsible for this alarm?
JSON:{
    "alerts": [
        {
            "annotations": {
                "description": "kube52.lbdaq.cern.ch is using too much ram 76.39337480022117%.",
                "summary": "kube52.lbdaq.cern.ch is using too much ram."
            },
            "endsAt": "2023-06-27T11:42:01.277Z",
            "fingerprint": "fc029f0c45c24ac2",
            "receivers": [
                {
                    "name": "aris"
                }
            ],
            "labels": {
                "alertname": "HighRamkUsage",
                "instance": "kube52.lbdaq.cern.ch",
                "job": "node-exporter",
                "notification_class": "aris",
                "resolve": "true",
                "severity": "critical"
            }
        }
    ],
    "labels": {
        "alertname": "HighRamkUsage"
    },
    "receiver": {
        "name": "aris"
    }
"""

print(pipe(query))