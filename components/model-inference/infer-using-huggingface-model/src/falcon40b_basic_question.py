from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch

torch_device = "cuda" if torch.cuda.is_available() else "cpu"
print(torch_device)

model_name = "tiiuae/falcon-40b-instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name, device_map="auto", trust_remote_code=True, load_in_8bit=True)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", trust_remote_code=True, load_in_8bit=True)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    trust_remote_code=True,
    device_map="auto",
)

prompt = f"""
what s the solution for each of the the hosts:
tfcfe01,p40_telegraf.service failed.,2023-06-28T00:38:10.518Z
n2232702,libceph: mds0 (1)10.128.108.137:6801 wrong peer at address,2023-06-28T00:38:11.641Z
n2232702,{7193}[Hardware Error]: event severity: corrected,2023-06-28T00:38:10.529Z
n2232702,{7193}[Hardware Error]:   node: 0 ,2023-06-28T00:38:11.218Z
n2232702,"{7193}[Hardware Error]:  Error 0, type: corrected",2023-06-28T00:38:10.530Z
n2232702,{7193}[Hardware Error]:  fru_text: DIMM ??,2023-06-28T00:38:10.531Z
n2232702,{7193}[Hardware Error]:   error_status: 0x0000000000000400,2023-06-28T00:38:11.218Z
n2023704,EDAC MC0: 1 CE memory read error on CPU_SrcID#1_Ha#0_Chan#1_DIMM#0 (channel:1 slot:0 page:0x93b4ce offset:0x9c0 grain:32 syndrome:0x0 -  area:DRAM err_code:0001:0091 socket:1 ha:0 channel_mask:2 rank:0),2023-06-28T00:38:10.566Z
n2232702,{7193}[Hardware Error]: It has been corrected by h/w and requires no further action,2023-06-28T00:38:10.529Z
n2232702,{7193}[Hardware Error]: Hardware error from APEI Generic Hardware Error Source: 0,2023-06-28T00:38:10.528Z
n2232702,{7193}[Hardware Error]:   section_type: memory error,2023-06-28T00:38:10.966Z
maeb04,"<warn>  [1687912700.1333] dnsmasq: spawn: dnsmasq process 1760252 exited with error: Network access problem (address in use, permissions) (2)",2023-06-28T00:38:20.133Z
tfcfe01,p40_telegraf.service failed.,2023-06-28T00:38:20.768Z
maeb04,"<warn>  [1687912700.1299] dnsmasq: spawn: dnsmasq process 1760251 exited with error: Network access problem (address in use, permissions) (2)",2023-06-28T00:38:20.129Z
maeb04,"<warn>  [1687912700.1357] dnsmasq: spawn: dnsmasq process 1760253 exited with error: Network access problem (address in use, permissions) (2)",2023-06-28T00:38:20.135Z
maeb04,"<warn>  [1687912700.1241] dnsmasq: spawn: dnsmasq process 1760249 exited with error: Network access problem (address in use, permissions) (2)",2023-06-28T00:38:20.124Z
maeb04,"<warn>  [1687912700.1273] dnsmasq: spawn: dnsmasq process 1760250 exited with error: Network access problem (address in use, permissions) (2)",2023-06-28T00:38:20.127Z
maeb04,<warn>  [1687912700.1358] dnsmasq[ceb195cffdc4eb96]: dnsmasq dies and gets respawned too quickly. Back off. Something is very wrong,2023-06-28T00:38:20.135Z
tfcfe01,"Cannot add dependency job for unit cvmfs-lhcb.cern.ch.mount, ignoring: Unit not found.",2023-06-28T00:38:25.752Z
gw29,falcoctl-artifact-follow.service failed.,2023-06-28T00:38:17.111Z
n2232702,{7194}[Hardware Error]: Hardware error from APEI Generic Hardware Error Source: 0,2023-06-28T00:38:20.847Z
n2232702,"{7194}[Hardware Error]:  Error 0, type: corrected",2023-06-28T00:38:21.923Z
n2232702,{7194}[Hardware Error]:   error_status: 0x0000000000000400,2023-06-28T00:38:22.109Z
n2232702,{7194}[Hardware Error]:   section_type: memory error,2023-06-28T00:38:22.108Z
n2232702,{7194}[Hardware Error]: It has been corrected by h/w and requires no further action,2023-06-28T00:38:20.848Z
n2232702,{7194}[Hardware Error]: event severity: corrected,2023-06-28T00:38:21.748Z
n2232702,{7194}[Hardware Error]:  fru_text: DIMM ??,2023-06-28T00:38:21.924Z
n2232702,{7194}[Hardware Error]:   node: 0 ,2023-06-28T00:38:22.110Z
"""

sequences = pipeline(
    prompt,
    max_length=1600,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
)
for seq in sequences:
    print(f"Result: {seq['generated_text']}")
