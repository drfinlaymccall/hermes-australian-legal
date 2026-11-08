"""Exercise a real historical lookup and after-record refusal, without printing law."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from au_legal.corpus import status, provision

p=argparse.ArgumentParser()
p.add_argument("--corpus",required=True)
a=p.parse_args()
root=Path(a.corpus).resolve()
def fingerprint():
    # Operator verification, not plugin runtime. Compare tracked status and HEAD.
    return subprocess.check_output(["git","-C",str(root),"status","--porcelain=v1"])+subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"])
before=fingerprint()
s=status(str(root))
r=provision(str(root),"competition-and-consumer-notification-of-acquisitions-determination-2025","s-1-9.md","2026-01-01")
try:
    provision(str(root),"competition-and-consumer-notification-of-acquisitions-determination-2025","s-1-9.md","2099-01-01")
except ValueError:
    refused=True
else:
    refused=False
assert refused, "After-record date was not refused"
assert fingerprint()==before,"Corpus changed during read-only proof"
print(json.dumps({"historical_lookup":"pass","date":r.get("date"),"corpus_commit":r.get("corpus_commit"),
 "compilation_commit":r.get("compilation_commit"),"text_sha256":hashlib.sha256(r['text'].encode()).hexdigest(),
 "record_to":s.get("record_to"),"caveats":r.get("caveats",[]),"after_record_refusal":refused,"corpus_unchanged":True,
 "boundary":"Historical lookup only; not current-law or legal-correctness validation."},indent=2))
