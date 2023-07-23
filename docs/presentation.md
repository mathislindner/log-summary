---
marp: true
paginate: true
---
<!-- _paginate: skip -->
# Leveraging the Power of Transfomers for Log Supervision
### Supervised by Aristeidis Fkiaras

A quick peek over the project I was assigned from mid-May to mid-July 2023

---
<!-- _paginate: skip -->
# Quick overview
1. Problem(s) at hand
2. Log Reduction
3. Logbook Reports
4. Future Work

---
# Problems at hand

- Logs can be tedious to read, even with good filters 
	- Similar messages but not exact matches, makes it harder to reduce the number of logs.
	- Can be very repetitive accross multiple hosts.
- Adding an entry to the logbook can be useful to keep track of the issues that could be encountered later, because we cannot store all of the logs forever.

---
# Log Reduction
To tackle the problem of repetetive logs we chose to use a sentence transformer to vectorise the logs and a hierarchical clustering to group similar logs together and send them back to opensearch as a new index each hour.


![word2vec, w:500](./images/downloaded_images/word2vec.png "title") ![hierarchical clustering,  width:500](./images/downloaded_images/hierarchical_clustering.png)

---

# Results on sytem logs errors and warnings
### Before
![before](./images/syslogserrorwarningbefore.PNG)
### After
![after](./images/syslogserrorwarningafter.PNG)

---
<font size="4">
<table class="table table-bordered table-hover table-condensed">
<thead><tr><th title="Field #1">host</th>
<th title="Field #2">message</th>
<th title="Field #3">n_unique_hosts</th>
<th title="Field #4">n_similar_messages</th>
<th title="Field #5">@timestamp</th>
<th title="Field #6">syslog_severity</th>
</tr></thead>
<tbody><tr>
<td>n2173301</td>
<td>igb 0000:06:00.0 eno1: Reset adapter</td>
<td>1</td>
<td align="right">2</td>
<td>2023-07-12 20:51:09.170000+00:00</td>
<td>error</td>
</tr>
<tr>
<td>n2173301</td>
<td>rcu: 	4-....: (1 GPs behind) idle=479/1/0x4000000000000000 softirq=15122273/15122274 fqs=455 </td>
<td>1</td>
<td align="right">3</td>
<td>2023-07-12 20:42:40.183000+00:00</td>
<td>error</td>
</tr>
<tr>
<td>n2173301</td>
<td>rcu: INFO: rcu_preempt self-detected stall on CPU</td>
<td>1</td>
<td align="right">7</td>
<td>2023-07-12 20:42:40.178000+00:00</td>
<td>error</td>
</tr>
<tr>
<td>n2081302</td>
<td>Error receiving audit netlink packet (No buffer space available)</td>
<td>1</td>
<td align="right">2</td>
<td>2023-07-12 16:20:17.934000+00:00</td>
<td>error</td>
</tr>
<tr>
<td>crguest14</td>
<td>Failed to enqueue OnFailure= job: Resource deadlock avoided</td>
<td>1</td>
<td align="right">2</td>
<td>2023-07-12 16:03:24.044000+00:00</td>
<td>error</td>
</tr>
<tr>
<td>megtestq1n1</td>
<td>usb 2-1-port1: over-current condition</td>
<td>1</td>
<td align="right">2</td>
<td>2023-07-12 15:50:40.459000+00:00</td>
<td>error</td>
</tr>
<tr>
<td>diri01</td>
<td>hid-generic 0003:03F0:034A.006C: usb_submit_urb(ctrl) failed: -19</td>
<td>1</td>
<td align="right">2</td>
<td>2023-07-12 15:24:31.224000+00:00</td>
<td>error</td>
</tr>
<tr>
<td>n2060301</td>
<td>Exiting the SSSD. Could not restart critical service [nss].</td>
<td>1</td>
<td align="right">7</td>
<td>2023-07-12 15:04:01.941000+00:00</td>
<td>error</td>
</tr>
</tbody></table>
</font>

---
# Logbook Reports
- Use the hourly summaries, re-vectorise them and cluster them again to get a summary of the day.
	- alot of logs also repeat throughout the day, so we can use the same method to reduce the number of logs again.
- Use an LLM to generate a summary of the day in sentences, while trying to keep the relevant information.
- We tried a few open-source models and ran them locally for privacy independency reasons, but the results were not satisfying.
- So for demonstration purposes we used the OpenAI's GPT-3.5

---
**System Log Report - July 12, 2023**

**Morning (00:00 - 08:59):**

The day began with several errors logged across different hosts. At midnight, the server n2201703 experienced a failure in the systemd-coredump service, resulting in a failed step and a read-only file system error. Another server, cronl03, reported a BIOS error related to the iwlwifi device.

In the early hours, the server lab14 encountered a forbidden error while checking for jobs, possibly due to access restrictions for the runner 'mv72UWrp.' Additionally, the server uceb13 reported a device detection error, suggesting the need for bus re-enumeration.

On cradm01, multiple issues occurred simultaneously. The process python2.7 was killed by an unsupported signal, the bluez5-util.c failed to retrieve ManagedObjects, and vdagent virtio channel access was denied... 

---
... Around 8:40 AM, uceb10 experienced an error related to network interface renaming, while crot02 failed to start the LSB service responsible for networking. A problem with the specified group 'plugdev' was also recorded on crot02.

**Late Morning (09:00 - 11:59):**

The server n6093103 encountered a connection refusal while attempting to send a WATCHDOG=1 notification message. Daqv0207 experienced a timeout while waiting for the primary device, and n8190704 reported a crash that was not saved in the specified file.

Meanwhile, loadbalancer-pluscc faced issues with the mailer process when attempting to mail the output of the `cron.daily` job. These errors might have affected the regular operation of the system.


---
# Future Work
<div class="container">
	<div style="width: 55%; float: left;">
		<ul>
		<li> Started working on the idea of a chatbot answering questions specific to the logs
		<li>  Main issue with this is finding the relevant information to the question:
			<ul>
				<li> Most LLM's do not support large inputs
				<li> This is usually tackled again with vectorisation and then cosine similarity search with the question but we do not have a good vectorisation for logs.
			</ul>
		<li> Train a good sentence transformer adapted for logs. (Most models are made to match things like synonyms and not log that are repetive)
		</ul>
	</div>
	<div class="image">
		<img src="./images/pipeline_for_llm.png"style="float: right;" alt="drawing" width=45%/>
	</div>

</div>

--- 
# Quick Demo of method 2
- Using Langchain module
	- Give the LLM a Prompt telling it how it can access a table and access its information
	- Tell it that it shouldanswer questions using a specific thought processes.
	- Add the relevant question after the prompt.
- Unfortunately there were limitations on the complexity of the question. The models we tried from huggingface would need more specific training on log understanding
	- The most complicated things you can ask is a simple, what happened to host xyz and it can find the logs specific to the question and summarize them a bit.

---
**Question**: What is the last log entry?
**Thought**: I should use the `sort_values` function to sort the dataframe by timestamp.
**Action**: python_repl_ast
**Action Input**: df.sort_values(by='@timestamp')
```	
Observation:             
host                                            message                        @timestamp
0     vedcsvss01  Failed to start backup_pvssInst.service.  2023-06-28 00:00:34.726000+00:00
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

---
**Thought**: I should use the `iloc` function to get the last row

**Action**: python_repl_ast

**Action** Input: df.sort_values(by='@timestamp').iloc[-1]

**Observation**: 
```
host                                                   n2232702
message       libceph: auth protocol 'cephx' mauth authentic...
@timestamp                     2023-06-28 12:14:32.605000+00:00
Name: 9999, dtype: object
```
**Thought**: I now know the final answer

**Final Answer**: n2232702


---
# Thank you for your attention

---
Technical slides

---
![daily hourly pipe](./images/daily_log_summary.png "title")
