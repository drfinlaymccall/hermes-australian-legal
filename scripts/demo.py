"""Print actual synthetic tool outputs. No model or legal conclusion."""
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from au_legal.workflow import review_gate, earnout

print(json.dumps({"fixture":"fictional_synthetic_only", "gate":review_gate(
    confidentiality_confirmed=True,privilege_reviewed=True,playbook_counsel_approved=False),
    "scenario":earnout(metric="125.50",threshold="100",rate="2.5",cap="1000")},indent=2))
