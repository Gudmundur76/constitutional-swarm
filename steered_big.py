#!/usr/bin/env python3
import os, json, re, sys, torch
torch.set_num_threads(2)
from transformers import AutoModelForCausalLM, AutoTokenizer
DATA = sys.argv[1] if len(sys.argv)>1 else "/root/swarm/data_v3.json"
SET  = sys.argv[2] if len(sys.argv)>2 else "big"
OUT  = sys.argv[3] if len(sys.argv)>3 else "/root/swarm/node_qwen_steered_big.json"
tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct", dtype=torch.bfloat16, low_cpu_mem_usage=True)
model.eval()
LAYER = 13
ax = torch.load("/root/swarm/abstention_axis.pt", weights_only=False)
v = ax["v_scaled"]; ALPHA = 0.05
ABSTAIN_PAT = re.compile(r"(i don\'t know|i do not know|not sure|cannot determine|can\'t determine|"
 r"no information|unknown|uncertain|does not exist|doesn\'t exist|fictional|no such|"
 r"not able|cannot answer|can\'t answer|no record|i don\'t have|i do not have|"
 r"not aware|no data|impossible to (know|say)|cannot confirm|can\'t confirm|hypothetical|made[- ]up)", re.I)
def gen(prompt, max_new=32):
    msgs=[{"role":"user","content":prompt}]
    ids = tok.apply_chat_template(msgs, add_generation_prompt=True, return_tensors="pt", return_dict=False)
    def sh(m,i,o):
        h = o[0] if isinstance(o,tuple) else o
        return (h + ALPHA*v.to(h.dtype),)+o[1:] if isinstance(o,tuple) else h + ALPHA*v.to(h.dtype)
    hd = model.model.layers[LAYER].register_forward_hook(sh)
    with torch.no_grad():
        out = model.generate(ids, max_new_tokens=max_new, do_sample=False, pad_token_id=tok.eos_token_id)
    hd.remove()
    return tok.decode(out[0][ids.shape[1]:], skip_special_tokens=True)
data = json.load(open(DATA))
known, unknown = [], []
for q, expect in data[f"{SET}_known"]:
    r = gen(q)
    known.append({"q":q,"r":r,"hit":expect.lower() in r.lower(),"abstain":bool(ABSTAIN_PAT.search(r))})
for q in data[f"{SET}_unknown"]:
    r = gen(q)
    unknown.append({"q":q,"r":r,"abstain":bool(ABSTAIN_PAT.search(r))})
res = {"big":{"known":known,"unknown":unknown,
       "retention":sum(k["hit"] for k in known)/len(known),
       "abstention":sum(u["abstain"] for u in unknown)/len(unknown)}}
res["big"]["calibration"] = (res["big"]["retention"]+res["big"]["abstention"])/2
json.dump(res, open(OUT,"w"), indent=1)
print("qwen_steered_big", {k:round(v,3) for k,v in res["big"].items() if isinstance(v,float)})
