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
| host                   | message                                                                                                                                                                                                                                                 | n_unique_hosts                    | n_similar_messages | @timestamp                       | syslog_severity                  |       |
|------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------|--------------------|----------------------------------|----------------------------------|-------|
| n2173301               | igb 0000:06:00.0 eno1: Reset adapter                                                                                                                                                                                                                    | 1                                 | 2                  | 2023-07-12 20:51:09.170000+00:00 | error                            |       |
| n2173301               | rcu: 	4-....: (1 GPs behind) idle=479/1/0x4000000000000000 softirq=15122273/15122274 fqs=455                                                                                                                                                            | 1                                 | 3                  | 2023-07-12 20:42:40.183000+00:00 | error                            |       |
| n2173301               | rcu: INFO: rcu_preempt self-detected stall on CPU                                                                                                                                                                                                       | 1                                 | 7                  | 2023-07-12 20:42:40.178000+00:00 | error                            |       |
| n2081302               | Error receiving audit netlink packet (No buffer space available)                                                                                                                                                                                        | 1                                 | 2                  | 2023-07-12 16:20:17.934000+00:00 | error                            |       |
| crguest14              | Failed to enqueue OnFailure= job: Resource deadlock avoided                                                                                                                                                                                             | 1                                 | 2                  | 2023-07-12 16:03:24.044000+00:00 | error                            |       |
| megtestq1n1            | usb 2-1-port1: over-current condition                                                                                                                                                                                                                   | 1                                 | 2                  | 2023-07-12 15:50:40.459000+00:00 | error                            |       |
| diri01                 | hid-generic 0003:03F0:034A.006C: usb_submit_urb(ctrl) failed: -19                                                                                                                                                                                       | 1                                 | 2                  | 2023-07-12 15:24:31.224000+00:00 | error                            |       |
| n2060301               | Exiting the SSSD. Could not restart critical service [nss].                                                                                                                                                                                             | 1                                 | 7                  | 2023-07-12 15:04:01.941000+00:00 | error                            |       |
| xxeb06                 | "    return MatMul8bitLt.apply(A, B, out, bias, state)"                                                                                                                                                                                                 | 1                                 | 4                  | 2023-07-12 15:02:55.937000+00:00 | error                            |       |
| xxeb06                 | RuntimeError: mat1 and mat2 shapes cannot be multiplied (1x1 and 2x8192)                                                                                                                                                                                | 1                                 | 2                  | 2023-07-12 15:02:55.937000+00:00 | error                            |       |
| crot03.lbdaq.cern.ch   | "tpm tpm0: [Firmware Bug]: TPM interrupt not working, polling instead"                                                                                                                                                                                  | 1                                 | 2                  | 2023-07-12 14:52:56.585000+00:00 | error                            |       |
| crot03.lbdaq.cern.ch   | thunderbolt 0000:03:00.0: failed to send driver ready to ICM                                                                                                                                                                                            | 1                                 | 4                  | 2023-07-12 14:52:56.584000+00:00 | error                            |       |
| xxeb06                 | "/usr/local/lib/python3.8/dist-packages/bitsandbytes/cuda_setup/main.py:149: UserWarning: WARNING: The following directories listed in your path were found to be non-existent: {PosixPath('http'), PosixPath('//lbproxy.cern.ch'), PosixPath('8080')}" | 1                                 | 10                 | 2023-07-12 13:01:32.858000+00:00 | error                            |       |
| xxeb06                 | 2023-07-12 13:01:16.278999: I tensorflow/core/platform/cpu_feature_guard.cc:182] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.                                                              | 1                                 | 4                  | 2023-07-12 13:01:16.279000+00:00 | error                            |       |
| loadbalancer-pluscc    | "Tried to mail output of job `cron.daily', but mailer process (/usr/sbin/sendmail) exited with status 71"                                                                                                                                               | 1                                 | 2                  | 2023-07-12 11:31:04.797000+00:00 | error                            |       |
| n8190704               | Not saving repeating crash in '/localdisk1/.vscode-server/extensions/ms-python.vscode-pylance-2023.5.30/dist/bundled/files/get_pytest_options.py'                                                                                                       | 2                                 | 3                  | 2023-07-12 09:19:50.953000+00:00 | error                            |       |
| daqv0207               | Timed out waiting for device 4 primary.                                                                                                                                                                                                                 | 1                                 | 2                  | 2023-07-12 09:08:54.378000+00:00 | error                            |       |
| n6093103               | Failed to send WATCHDOG=1 notification message: Connection refused                                                                                                                                                                                      | 3                                 | 4                  | 2023-07-12 09:08:39.336000+00:00 | error                            |       |
| lhcbasus01             | sep5_39: Driver loading...                                                                                                                                                                                                                              | 1                                 | 11                 | 2023-07-12 08:43:30.877000+00:00 | error                            |       |
| lhcbasus01             | failed to execute '/usr/lib/udev/bwnotify' 'bwnotify 3-2.4': No such file or directory                                                                                                                                                                  | 1                                 | 5                  | 2023-07-12 08:43:23.843000+00:00 | error                            |       |
| lhcbasus01             | i2c i2c-0: sendbytes: NAK bailout.                                                                                                                                                                                                                      | 1                                 | 5                  | 2023-07-12 08:43:21.260000+00:00 | error                            |       |
| uceb10                 |                                                                                                                                                                                                                                                         | 1                                 | 2                  | 2023-07-12 08:40:16.663000+00:00 | error                            |       |
| uceb10                 | "uverbs0: /etc/udev/rules.d/90-ib.rules:4 Only network interfaces can be renamed                                                                                                                                                                        | ignoring NAME=""infiniband/%k""." | 1                  | 2                                | 2023-07-12 08:40:15.931000+00:00 | error |
| crot02                 | Failed to start LSB: Bring up/down networking.                                                                                                                                                                                                          | 2                                 | 3                  | 2023-07-12 08:37:47.770000+00:00 | error                            |       |
| crot02                 | '/var/spool/abrt/ccpp-2023-05-08-13:18:27-9441' is not a problem directory                                                                                                                                                                              | 1                                 | 7                  | 2023-07-12 08:37:41.291000+00:00 | error                            |       |
| crot02                 | specified group 'plugdev' unknown                                                                                                                                                                                                                       | 2                                 | 3                  | 2023-07-12 08:37:39.439000+00:00 | error                            |       |
| cradm01                | Process 9025 (python2.7) of user 0 killed by signal 3 - ignoring (unsupported signal)                                                                                                                                                                   | 5                                 | 11                 | 2023-07-12 08:05:06.097000+00:00 | error                            |       |
| cradm01                | [pulseaudio] bluez5-util.c: GetManagedObjects() failed: org.freedesktop.systemd1.NoSuchUnit: Unit not found.                                                                                                                                            | 4                                 | 6                  | 2023-07-12 08:05:01.321000+00:00 | error                            |       |
| cradm01                | No credentials cache found (filename: /tmp/krb5cc_10140_we5YXz)                                                                                                                                                                                         | 6                                 | 7                  | 2023-07-12 08:04:57.383000+00:00 | error                            |       |
| cradm01                | Cannot access vdagent virtio channel /dev/virtio-ports/com.redhat.spice.0                                                                                                                                                                               | 7                                 | 20                 | 2023-07-12 08:04:47.552000+00:00 | error                            |       |
| lbonluix               | [ERROR] sesman_data_in: scp_process_msg failed                                                                                                                                                                                                          | 1                                 | 20                 | 2023-07-12 07:51:39.766000+00:00 | error                            |       |
| utdcs01                | Preauthentication failed                                                                                                                                                                                                                                | 16                                | 30                 | 2023-07-12 06:55:40.222000+00:00 | error                            |       |
| crguest03              | gkr-pam: the password for the login keyring was invalid.                                                                                                                                                                                                | 3                                 | 10                 | 2023-07-12 06:50:33.838000+00:00 | error                            |       |
| crguest03              | Out of memory: Kill process 6614 (gnome-shell) score 554 or sacrifice child                                                                                                                                                                             | 2                                 | 7                  | 2023-07-12 06:37:23.079000+00:00 | error                            |       |
| cronl02                | [drm:intel_cpu_fifo_underrun_irq_handler [i915]] *ERROR* CPU pipe A FIFO underrun                                                                                                                                                                       | 5                                 | 11                 | 2023-07-12 04:33:30.309000+00:00 | error                            |       |
| lab18                  | activemq.rb:134:in `on_miscerr' Unexpected error on connection stomp+ssl://server@mcoactivemq01.lbdaq.cern.ch:61614: es_oldrecv: receive failed: Connection reset by peer                                                                               | 5                                 | 13                 | 2023-07-12 02:34:25.443000+00:00 | error                            |       |
| n8190404               | Process 16563 (.nfs00000000c0845eb20000000a) of user 10297 killed by SIGSEGV - dumping core                                                                                                                                                             | 10                                | 18                 | 2023-07-12 02:25:03.687000+00:00 | error                            |       |
| n2100701.lbdaq.cern.ch | x86/cpu: VMX (outside TXT) disabled by BIOS                                                                                                                                                                                                             | 2                                 | 3                  | 2023-07-12 02:16:38.191000+00:00 | error                            |       |
| acctb01                | "[/usr/local/lib/systemd/system/xpra.service:15] Failed to parse protect system value, ignoring: strict"                                                                                                                                                | 1                                 | 13                 | 2023-07-12 01:46:57.703000+00:00 | error                            |       |
| pleb01                 | i2c i2c-2: Failed reset at end of transaction (01)                                                                                                                                                                                                      | 4                                 | 17                 | 2023-07-12 01:43:39.775000+00:00 | error                            |       |
| n4061001               | "Failed to query NVIDIA devices. Please ensure that the NVIDIA device files (/dev/nvidia*) exist, and that user 0 has read and write permissions for those files."                                                                                      | 2                                 | 26                 | 2023-07-12 01:41:10.619000+00:00 | error                            |       |
| n2101504               | INFO: task auditd:1170 blocked for more than 122 seconds.                                                                                                                                                                                               | 3                                 | 8                  | 2023-07-12 01:21:52.843000+00:00 | error                            |       |
| n2103101               | FS-Cache: O-cookie d=00000000d29b9d7b n=000000006079bde2                                                                                                                                                                                                | 16                                | 92                 | 2023-07-12 01:13:51.620000+00:00 | error                            |       |
| n2103102               | could not read from '/sys/module/acpi_cpufreq/initstate': No such device                                                                                                                                                                                | 3                                 | 4                  | 2023-07-12 01:13:44.436000+00:00 | error                            |       |
| vedcsvss01             | Failed to start backup_pvssInst.service.                                                                                                                                                                                                                | 100                               | 109                | 2023-07-12 01:10:10.590000+00:00 | error                            |       |
| graphite02             | "ts=2023-07-12T01:00:28.056Z caller=compact.go:519 level=info component=tsdb msg=""write block"" mint=1689112813014 maxt=1689120000000 ulid=01H53ST8ZKFG6M0KRFP7DNX17W duration=36.227905ms"                                                            | 2                                 | 46                 | 2023-07-12 01:00:28.056000+00:00 | error                            |       |
| n2081302               | Failed to start User Manager for UID 0.                                                                                                                                                                                                                 | 3                                 | 18                 | 2023-07-12 00:35:26.476000+00:00 | error                            |       |
| n2043902               | (lhcb.cern.ch) watchdog: received unexpected signal 15 from PID 1 / UID 0                                                                                                                                                                               | 13                                | 70                 | 2023-07-12 00:26:28.073000+00:00 | error                            |       |
| n2043902               | Failed to connect to coredump service: Connection refused                                                                                                                                                                                               | 9                                 | 17                 | 2023-07-12 00:26:27.575000+00:00 | error                            |       |
| saeb16                 | LHCb_SAEB16_BU_1 BU: Incomplete event! No data received from the following sources: 0x102f/vatel052_1 0x1032/vatel053_0 0x1033/vatel053_1                                                                                                               | 85                                | 222                | 2023-07-12 00:16:15.792000+00:00 | error                            |       |
| xxeb02                 | dnsd.service: Failed at step EXEC spawning /usr/bin/dns: No such file or directory                                                                                                                                                                      | 2                                 | 49                 | 2023-07-12 00:05:26.127000+00:00 | error                            |       |
| loadbalancer-pluscc    | libceph: bad option at 'mds_namespace=calib'                                                                                                                                                                                                            | 5                                 | 61                 | 2023-07-12 00:02:55.543000+00:00 | error                            |       |
| loadbalancer-pluscc    | "(lhcb.cern.ch) decompressing /data/ba/9338e08e3fda4f40e3f3f51b17e29aeee51160C, local IO error"                                                                                                                                                         | 1                                 | 61                 | 2023-07-12 00:02:20.713000+00:00 | error                            |       |
| n2201703               | systemd-coredump@23-2972395-0.service: Failed at step NAMESPACE spawning /usr/lib/systemd/systemd-coredump: Read-only file system                                                                                                                       | 4                                 | 23                 | 2023-07-12 00:02:05.089000+00:00 | error                            |       |
| cronl03                | iwlwifi 0000:00:14.3: BIOS contains WGDS but no WRDS                                                                                                                                                                                                    | 2                                 | 26                 | 2023-07-12 00:01:25.576000+00:00 | error                            |       |
| n2201703               | Aborted                                                                                                                                                                                                                                                 | 8                                 | 201                | 2023-07-12 00:01:01.091000+00:00 | error                            |       |
| n2201703               | Can't open timestamp file for job cron.daily: Read-only file system                                                                                                                                                                                     | 2                                 | 6                  | 2023-07-12 00:01:01.091000+00:00 | error                            |       |
| uceb13                 | "P40:pcie40_probe(): device detected but unreadable, please re-enumerate bus to continue"                                                                                                                                                               | 3                                 | 26                 | 2023-07-12 00:00:08.940000+00:00 | error                            |       |
| lab14                  | ERROR: Checking for jobs... forbidden               runner=mv72UWrp                                                                                                                                                                                     | 3                                 | 232                | 2023-07-12 00:00:05.283000+00:00 | error                            |       |

### Here is the generated daily report by GPT-3.5
```
Daily Logbook - 12/07/2023

Date: 12/07/2023

Today, I reviewed the system logs to identify any critical errors or issues that could affect the functioning of the system. Here is a summary of the significant events:

Host n2173301 reported a network adapter reset, which may indicate a potential network connectivity problem.
Host n2081302 encountered an issue with receiving audit netlink packets due to a lack of buffer space, potentially affecting audit functionality.
Host crguest14 experienced a resource deadlock while enqueuing a job, requiring further investigation to prevent similar occurrences.
Host n2060301 faced a critical issue with the SSSD, resulting in the system's exit and a failure to restart the critical service "nss."
Host xxeb06 raised errors related to TensorFlow and CUDA setup, which could impact specific functionalities dependent on these frameworks.
Host crot03.lbdaq.cern.ch encountered a firmware bug related to the TPM interrupt not working properly, requiring attention to ensure proper TPM functionality.
Host lhcbasus01 faced various errors, including driver loading, failure to execute specific commands, and I2C communication errors.
Host crot02 encountered issues with networking services and specified groups, indicating potential configuration or system setup problems.
Host cradm01 reported errors related to signal handling, pulseaudio, credentials cache, and vdagent virtio channel access.
Host utdcs01 experienced preauthentication failures, suggesting authentication issues that need to be resolved.
Host crguest03 encountered errors related to the login keyring password and process kills due to memory exhaustion, requiring further investigation.
Host lab18 raised an unexpected error while connecting to an ActiveMQ server, indicating a possible network or server issue.
Host n8190404 faced a process killed by a segmentation fault, leading to a core dump.
Host n4061001 encountered issues querying NVIDIA devices, which could impact GPU-related functionalities.
Host n2101504 reported a task blocked for an extended period, indicating potential performance issues that should be investigated.
Host n2103101 encountered an FS-Cache error related to an O-cookie, which might affect file system caching.
Host vedcsvss01 faced a failure to start the backup_pvssInst.service, potentially impacting the backup process.
Host graphite02 experienced errors related to the write block process and local I/O error during decompression, requiring further analysis.
Host n2201703 encountered various errors, including failed namespace step, aborted processes, and read-only file system issues.
Host cronl03 raised an error regarding the presence of WGDS in the BIOS without WRDS support.
Host uceb13 encountered an error related to an unreadable P40 device, requiring re-enumeration of the bus.
End of Daily Logbook - 12/07/2023
```

## Image of the pipeline
#include image of the pipeline
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
