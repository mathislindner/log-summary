# Summarise System Logs from CERN LHCB's using Transformers
## Description
This repository contains two projects:
One part is about taking the system logs of the CERN LHCB, summarising it by hour using a sentence transformer and clustering the results.
The other resummarises the logs by day and then creates a daily report using an LLM.

## Results
### Hourly Reindexing
This is the compression we got for approximately 10 hours of logs:
Dashboard before:
![Hourly reindexing before](/docs/images/syslogserrorwarningbefore.PNG)
Dashboard after:
![Hourly reindexing after](/docs/images/syslogserrorwarningafter.PNG)
### Daily Reports
Unfortunately the LLM's Falcon40B and LLama65b were not as good as we hoped. But the proof of concept stands, after taking the daily clustered logs (approximately 100-200 entries) and running them with GPT-4 we get the following results:
As soon as a better LLM on Huggingface is available, we can easily switch it out and get better results.

#include table and a daily report of the day to show 

## Image of the pipeline
#include image of the pipeline
![Daily summary pipeline](/docs/images/daily_log_summary.png)

## Run the jobs
### Run hourly Reindexing
To run the hourly reindexing, simply run a cron job with the following command hourly:
```
bash run_hourly_reindexing.sh this/is/your/path/log-summary /wherever/you/want/the/cache/to/be false
```
You will have to build the docker containers on the first run by changing the last argument to true.

### Run Daily Reports
This part has to be run in parallel to the hourly reindexing. To run the daily reports: It uses the hourly reindexing cache to create a daily report. To run the daily reports, simply run compose up.
```
docker-compose up
```

## Side notes
### Langchain Agent
#### Idea
![Langchain Agent Pipeline](/docs/images/pipeline_for_llm.png)
At some point an idea came up to create a bot that answers questions about the logs, unfortunately we could not find a model that does the job well enough of answering the questions right away. So we tried using agents, where the our best conversation was as follows:

#### Example Conversation
Question: What is the last log entry?

Thought: I should use the `sort_values` function to sort the dataframe by timestamp.
Action: python_repl_ast
Action Input: df.sort_values(by='@timestamp')
```	
Observation:             
host                                            message                        @timestamp
0     vedcsvss01           Failed to start backup_pvssInst.service.  2023-06-28 00:00:34.726000+00:00
1         crot03  iwlwifi 0000:00:14.3: BIOS contains WGDS but n...  2023-06-28 00:00:39.239000+00:00
2       n4061401  ERROR: Checking for jobs... forbidden  ...  2023-06-28 00:00:55.171000+00:00
3       n4061401  ERROR: Runner https://gitlab.cern.ch/zs...  2023-06-28 00:00:55.923000+00:00
4       n4061401  ERROR: Checking for jobs... forbidden  ...  2023-06-28 00:01:55.200000+00:00
...          ...                                                ...                               ...
9995    n2232702  libceph: auth protocol 'cephx' mauth authentic...  2023-06-28 12:14:22.365000+00:00
9996    n2232702  libceph: auth protocol 'cephx' mauth authentic...  2023-06-28 12:14:22.388000+00:00
9997    n2232702  libceph: auth protocol 'cephx' mauth authentic...  2023-06-28 12:14:25.460000+00:00
9998    n2232702  libceph: auth protocol 'cephx' mauth authentic...  2023-06-28 12:14:32.605000+00:00
9999    n2232702  libceph: auth protocol 'cephx' mauth authentic...  2023-06-28 12:14:32.605000+00:00
[10000 rows x 3 columns]
```
Thought: I should use the `iloc` function to get the last row.
Action: python_repl_ast
Action Input: df.sort_values(by='@timestamp').iloc[-1]
Observation: 
```
host                                                   n2232702
message       libceph: auth protocol 'cephx' mauth authentic...
@timestamp                     2023-06-28 12:14:32.605000+00:00
Name: 9999, dtype: object
```
Thought: I now know the final answer
Final Answer: n2232702
