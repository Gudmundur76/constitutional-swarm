#!/usr/bin/env python3
import json, subprocess, sys, time, re, urllib.request, os

LLAMA = "/root/swarm/llama-b10068/llama-server"
MODELS = {
 "bonsai8b":  "/root/swarm/models/Bonsai-8B-Q1_0.gguf",
 "qwen05b":   "/root/swarm/models/qwen2.5-0.5b-instruct-q8_0.gguf",
 "smollm360": "/root/swarm/models/smollm2-360m-instruct-q8_0.gguf",
}
ABSTAIN_PAT = re.compile(r"(i don\'t know|i do not know|not sure|cannot determine|can\'t determine|"
 r"no information|unknown|uncertain|does not exist|doesn\'t exist|fictional|no such|"
 r"not able|cannot answer|can\'t answer|no record|i don\'t have|i do not have|"
 r"not aware|no data|impossible to (know|say)|cannot confirm|can\'t confirm|hypothetical|made[- ]up)", re.I)

def ask(port, q, max_tokens=32):
    body = json.dumps({"messages":[{"role":"user","content":q}], "max_tokens":max_tokens, "temperature":0}).encode()
    req = urllib.request.Request(f"http://127.0.0.1:{port}/v1/chat/completions", data=body,
                                 headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"].strip()

def run_model(name, path, port, sets):
    proc = subprocess.Popen([LLAMA, "-m", path, "--port", str(port), "-c", "2048", "-t", "2",
                             "--no-warmup", "--log-disable"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(120):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=2); break
            except Exception: time.sleep(2)
        data = json.load(open(sys.argv[3] if len(sys.argv)>3 else "/root/swarm/data.json"))
        out = {}
        for s in sets:
            known, unknown = [], []
            for q, expect in data[f"{s}_known"]:
                r = ask(port, q)
                known.append({"q":q,"r":r,"hit":expect.lower() in r.lower(),"abstain":bool(ABSTAIN_PAT.search(r))})
            for q in data[f"{s}_unknown"]:
                r = ask(port, q)
                unknown.append({"q":q,"r":r,"abstain":bool(ABSTAIN_PAT.search(r))})
            out[s] = {"known":known,"unknown":unknown,
                      "retention":sum(k["hit"] for k in known)/len(known),
                      "abstention":sum(u["abstain"] for u in unknown)/len(unknown)}
            out[s]["calibration"] = (out[s]["retention"]+out[s]["abstention"])/2
        json.dump(out, open(f"/root/swarm/node_{name}.json","w"), indent=1)
        print(name, {s:{k:round(out[s][k],3) for k in ("retention","abstention","calibration")} for s in sets})
    finally:
        proc.terminate(); proc.wait()

if __name__ == "__main__":
    name = sys.argv[1]; sets = sys.argv[2].split(",") if len(sys.argv)>2 else ["probe","holdout"]
    run_model(name, MODELS[name], 8891, sets)
