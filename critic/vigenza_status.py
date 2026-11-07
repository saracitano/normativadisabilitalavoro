#!/usr/bin/env python3
"""Critic di vigenza: legge audit pubblicato, non inventa esiti legali.

Uso:
 python3 -m critic.vigenza_status --id L68-1999
 python3 -m critic.vigenza_status --all
"""
import argparse
import json
from pathlib import Path

AUDIT = Path(__file__).with_name("audit-vigenza-2026-11-08.json")

def load_report(path=AUDIT):
    report=json.loads(Path(path).read_text(encoding="utf-8"))
    ids=[x["id"] for x in report["records"]]
    if len(ids)!=len(set(ids)): raise ValueError("ID duplicati")
    if report["risultati"]["totale"]!=len(ids): raise ValueError("Totale incoerente")
    return report

def interpret(record):
    return {
       "id":record["id"],"title":record["titolo"],
       "act_status":record["stato_atto"],
       "article_status":record["stato_articoli"],
       "individual_applicability":record["applicabilita"],
       "source":record["fonte_consultata"],
       "evidence_note":record["nota"],
       "date":record["data_audit"],
       "can_claim_current_article":False,
       "decision":"Non presentare come diritto applicabile senza controllo puntuale di articolo, versione, data e requisiti."
    }

def main():
    p=argparse.ArgumentParser()
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument("--id")
    group.add_argument("--all",action="store_true")
    p.add_argument("--report",default=str(AUDIT))
    args=p.parse_args()
    report=load_report(args.report)
    if args.all:
       data=[interpret(x) for x in report["records"]]
    else:
       data=[interpret(x) for x in report["records"] if x["id"]==args.id]
       if not data: raise SystemExit("Atto non presente nell'audit")
    print(json.dumps({"audit_date":report["data"],"count":len(data),"records":data},
                     ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
