#!/usr/bin/env python3
import json, random
random.seed(42)
nodes = {}
for n,f in [("bonsai8b","node_bonsai8b.json"),("qwen05b","node_qwen05b.json"),
            ("smollm360","node_smollm360.json"),("qwen_steered","node_qwen_steered_big.json")]:
    try: nodes[n] = json.load(open("/root/swarm/"+f))
    except Exception as e: print("missing", n)
def cal(members, vetoers, ik=None, iu=None):
    m0=members[0]
    nk=len(nodes[m0]["big"]["known"]); nu=len(nodes[m0]["big"]["unknown"])
    ik=ik if ik is not None else range(nk); iu=iu if iu is not None else range(nu)
    rn=0; rd=0
    for i in ik:
        rd+=1
        if not any(nodes[m]["big"]["known"][i]["abstain"] for m in vetoers):
            hits=[nodes[m]["big"]["known"][i]["hit"] for m in members if not nodes[m]["big"]["known"][i]["abstain"]]
            if hits and sum(hits)>len(hits)/2: rn+=1
    an=sum(1 for i in iu if any(nodes[m]["big"]["unknown"][i]["abstain"] for m in vetoers))
    iu=list(iu)
    r=rn/max(rd,1); a=an/max(len(iu),1)
    return r,a,(r+a)/2
def boot(members,vetoers,iters=2000):
    m0=members[0]
    nk=len(nodes[m0]["big"]["known"]); nu=len(nodes[m0]["big"]["unknown"])
    cs=[]
    for _ in range(iters):
        ik=[random.randrange(nk) for _ in range(nk)]; iu=[random.randrange(nu) for _ in range(nu)]
        cs.append(cal(members,vetoers,ik,iu)[2])
    cs.sort(); return cs[int(.025*iters)], cs[int(.975*iters)]
print("nodes:",sorted(nodes))
for m in sorted(nodes):
    d=nodes[m]["big"]
    print(f"  single {m:14s} ret={d['retention']:.3f} abs={d['abstention']:.3f} cal={d['calibration']:.3f}")
MEM=["bonsai8b","qwen05b","smollm360"]
for tag,mem,vet in [("dual-veto (B&Q)",MEM,["bonsai8b","qwen05b"]),
                    ("triple-veto (B&Q&Steer)",MEM+["qwen_steered"],["bonsai8b","qwen05b","qwen_steered"])]:
    if all(m in nodes for m in mem+vet):
        r,a,c=cal(mem,vet); lo,hi=boot(mem,vet)
        print(f"  {tag:26s} ret={r:.3f} abs={a:.3f} cal={c:.3f}  95%CI=[{lo:.3f},{hi:.3f}]")
