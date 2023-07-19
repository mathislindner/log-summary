---
marp: true
---

# Leveraging the Power of Transfomers
# for Log Supervision


A quick overview over the project I was assigned from May to July 2023

---
# Quick overview
1. Problem at hand
2. Log Reduction
    - Hourly
    - Daily
3. Logbook Reports
4. Future Work

---
# Problems at hand
- Logs can be tedious to read, even with a good filters such as opensearch: 
    - similar messages but not exact match makes it harder to filter.
    - very repetitive on one or multiple hosts.
- Adding an entry to the logbook can be useful to keep track of the issues that could be encountered later, but we cannot store them forever.
- It can be easier to inteact with the logs with plain text

---
# Log Reduction
To tackle the problem of 
---
---

![daily hourly pipe](./images/daily_log_summary.png "title")

---

# Results on sytem logs errors and warnings
### Errors and  before
![before](./images/syslogserrorwarningbefore.PNG)
### Errors after
![after](./images/syslogserrorwarningafter.PNG)

---
# Future Work

- Also worked on the idea of a chatbot answering questions specific to the logs
- Main issue with this is finding the relevant information to the question:
    - LLM do not support huge inputs
    - This is usually tackled with vectorisation and similarity search with the question
- Things to improve: train a good vectorization adapted for logs. (Most models are made to understanding synonyms and not log similarities)
#add image of pipeline
--- 
# Method 2 Implementation and example

Give the LLM a Prompt telling it how it can access a table and access its information
Tell it how it should go through with thought processes.
Add the relevant question.
Let it generate sequentially new “thoughts”

---
- Using Langchain module
- Limitations on the complexity of the question. Need more specific training on log understanding
- The most complicated things you can ask is a simple, what happened to host xyz and it can find the logs specific to the question and summarize them a bit.
- The problem is if too many things happened, not everything can fit in the model input, so there needs to be a form a compression.
#add image of conv
---
# Thank you for your attention
