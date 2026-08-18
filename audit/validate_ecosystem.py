#!/usr/bin/env python3
import json,os,sys,urllib.request
from pathlib import Path
ORDER={"FALSIFIED":0,"OPEN":1,"PREDICTED":2,"VERIFIED":3,"FORMALIZED":4,"PROVEN":5}
REQ={"id","claim","type","deps","proof","code","dataset","hash","result","status"}
def validate(data,label):
 if data.get('ledger')!='QCAL Ω Audit Ledger' or data.get('version')!='1.0.1': raise ValueError(f'{label}: invalid ledger header')
 by={}
 for e in data.get('entries',[]):
  miss=REQ-set(e)
  if miss: raise ValueError(f'{label}:{e.get("id")}: missing {sorted(miss)}')
  if e['status'] not in ORDER: raise ValueError(f'{label}:{e["id"]}: invalid status')
  if e['id'] in by: raise ValueError(f'{label}: duplicate {e["id"]}')
  by[e['id']]=e
 for e in data['entries']:
  for d in e['deps']:
   if d.startswith('AXIOM_'): continue
   if d not in by: raise ValueError(f'{label}:{e["id"]}: unknown dependency {d}')
   if ORDER[e['status']]>ORDER[by[d]['status']]: raise ValueError(f'{label}:{e["id"]}: inheritance violation via {d}')
 return len(by)
def main():
 manifest=json.loads(Path('audit/ecosystem_manifest.json').read_text(encoding='utf8'))
 ref=os.environ.get('AUDIT_REF', 'main')
 total=0
 for repo in manifest['repositories']:
  url=f"https://raw.githubusercontent.com/motanova84/{repo['name']}/{ref}/ledger/omega.json"
  with urllib.request.urlopen(url,timeout=30) as r: data=json.load(r)
  n=validate(data,repo['name']); total+=n; print(f'PASS {repo["name"]}@{ref}: {n} entries')
 print(f'QCAL Ω ecosystem audit PASS: {total} entries across {len(manifest["repositories"])} repositories')
if __name__=='__main__':
 try: main()
 except Exception as e: print('ERROR:',e,file=sys.stderr);sys.exit(1)
