# Summarise System Logs from CERN LHCB's using Transformers
# Description
This repository contains two projects:
One part is about taking the system logs of the CERN LHCB, summarising it by hour using a sentence transformer and clustering the results.
The other resummarises the logs by day and then creates a daily report using an LLM.

# Results
## Hourly Reindexing
This is the compression we got for approximately 10 hours of logs:
Dashboard before:
![Hourly reindexing before](/docs/images/syslogserrorwarningbefore.PNG)
Dashboard after:
![Hourly reindexing after](/docs/images/syslogserrorwarningafter.PNG)
## Daily Reports
Unfortunately the LLM's Falcon40B and LLama65b were not as good as we hoped. But the proof of concept stands, after taking the daily clustered logs (approximately 100-200 entries) and running them with GPT-3.5 we get the following results:
As soon as a better LLM on Huggingface is available, we can easily switch it out and get better results.

### Table of the compressed logs on that day:
You can find the csv that generated the report bloew in examples/compressed_daily_error.csv

### Here is the generated daily report by GPT-3.5

**System Log Report - July 12, 2023**

**Morning (00:00 - 08:59):**

The day began with several errors logged across different hosts. At midnight, the server n2201703 experienced a failure in the systemd-coredump service, resulting in a failed step and a read-only file system error. Another server, cronl03, reported a BIOS error related to the iwlwifi device.

In the early hours, the server lab14 encountered a forbidden error while checking for jobs, possibly due to access restrictions for the runner 'mv72UWrp.' Additionally, the server uceb13 reported a device detection error, suggesting the need for bus re-enumeration.

On cradm01, multiple issues occurred simultaneously. The process python2.7 was killed by an unsupported signal, the bluez5-util.c failed to retrieve ManagedObjects, and vdagent virtio channel access was denied.

Around 8:40 AM, uceb10 experienced an error related to network interface renaming, while crot02 failed to start the LSB service responsible for networking. A problem with the specified group 'plugdev' was also recorded on crot02.

**Late Morning (09:00 - 11:59):**

The server n6093103 encountered a connection refusal while attempting to send a WATCHDOG=1 notification message. Daqv0207 experienced a timeout while waiting for the primary device, and n8190704 reported a crash that was not saved in the specified file.

Meanwhile, loadbalancer-pluscc faced issues with the mailer process when attempting to mail the output of the `cron.daily` job. These errors might have affected the regular operation of the system.

**Afternoon (12:00 - 17:59):**

During the afternoon, errors were recorded on multiple hosts. The server xxeb06 raised warnings related to non-existent directories in the path and a runtime error caused by incompatible matrix shapes in TensorFlow.

Crot03.lbdaq.cern.ch reported problems with the TPM interrupt, resorting to polling instead. Additionally, the thunderbolt driver on the same server failed to send a driver ready signal to ICM (Intel Connection Manager).

The server lhcbasus01 encountered driver loading issues, failed to execute bwnotify due to a missing file, and faced a sendbytes error on the i2c interface.

N2060301 experienced critical issues with the SSSD, resulting in the failure to restart the critical nss service. This problem could have affected the system's authentication and user resolution capabilities.

**Evening (18:00 - 23:59):**

The server crguest14 encountered a resource deadlock avoided error, while n2081302 reported an error related to the audit netlink packet receiving process due to insufficient buffer space. These errors might have affected the respective functionalities of the systems.

Late in the evening, n2173301 experienced multiple errors, including a reset adapter event and an RCU self-detected stall on the CPU. These errors could have had an impact on the network adapter's functionality and the CPU's performance.

Overall, today's logs indicate a variety of errors across different servers, highlighting potential issues with network adapters, CPU performance, service restarts, missing files, device communication, and system resources. Further investigation and resolution of these errors are essential to maintain the stability and proper functioning of the system.

## Image of the pipeline
![Daily summary pipeline](/docs/images/daily_log_summary.png)

# Run the jobs
## Run hourly Reindexing
To run the hourly reindexing, simply run a cron job with the following command hourly:
```
bash run_hourly_reindexing.sh this/is/your/path/log-summary /wherever/you/want/the/cache/to/be false
```
You will have to build the docker containers on the first run by changing the last argument to true.

## Run Daily Reports
This part has to be run in parallel to the hourly reindexing. To run the daily reports: It uses the hourly reindexing cache to create a daily report. To run the daily reports, simply run compose up.
```
docker-compose up
```

# Side notes
## Langchain Agent
### Idea
![Langchain Agent Pipeline](/docs/images/pipeline_for_llm.png)
At some point an idea came up to create a bot that answers questions about the logs, unfortunately we could not find a model that does the job well enough of answering the questions right away. So we tried using agents, where the our best conversation was as follows:

## Example Conversation
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
Thought: I should use the `iloc` function to get the last row

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
