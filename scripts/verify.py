"""Run reproducible software gates; report actual outputs, never legal accuracy."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--corpus',help='Optional reviewed local corpus for historical integration')
    args=parser.parse_args()
    commands=[
        [sys.executable,'-m','unittest','discover','-s','tests','-v'],
        [sys.executable,'scripts/demo.py'],
        ['hermes','plugins','doctor',str(ROOT),'--ci'],
        ['hermes','plugins','validate',str(ROOT),'--json'],
    ]
    if args.corpus:
        commands.append([sys.executable,'scripts/corpus-smoke.py','--corpus',args.corpus])
    results=[]
    for command in commands:
        done=subprocess.run(command,cwd=ROOT,text=True,capture_output=True,timeout=180)
        # Caller controls whether to retain this output; no private deal files are read.
        label=' '.join(command[1:]) if command[0]==sys.executable else ' '.join(command[:3])
        label=label.replace(str(ROOT),'<plugin>').replace(args.corpus or '\0','<corpus>')
        results.append({'command':label,'exit_code':done.returncode,
                        'stdout':done.stdout,'stderr':done.stderr})
    source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in sorted(ROOT.rglob('*.py')) if '.git' not in p.parts}
    print(json.dumps({'scope':'software_contract_and_historical_integration_only',
                      'all_passed':all(x['exit_code']==0 for x in results),
                      'results':results,'python_source_sha256':source_hashes},indent=2))
    return 0 if all(x['exit_code']==0 for x in results) else 1


if __name__=='__main__':
    raise SystemExit(main())
