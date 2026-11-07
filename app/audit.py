#!/usr/bin/env python3
"""Auditor read-only dell'integrità e dello stato di copertura normativa."""
import argparse
import json
from datetime import date
from .legislation import connect
from .official_ingest import SCHEMA

def audit(db, as_of):
    db.executescript(SCHEMA)
    acts=db.execute("SELECT id,title,source_url FROM acts ORDER BY id").fetchall()
    result=[]
    for act_id,title,url in acts:
        n=db.execute("SELECT COUNT(*) FROM articles WHERE act_id=?",(act_id,)).fetchone()[0]
        docs=db.execute("SELECT COUNT(*) FROM official_documents WHERE act_id=?",(act_id,)).fetchone()[0]
        versions=db.execute("SELECT COUNT(*) FROM official_versions WHERE act_id=?",(act_id,)).fetchone()[0]
        reviews=db.execute("""SELECT outcome,as_of,reviewer FROM legal_reviews
            WHERE act_id=? AND as_of<=? ORDER BY as_of DESC,review_date DESC LIMIT 1""",
            (act_id,as_of)).fetchone()
        flag="non_implementato" if not docs else ("revisione_umana_presente" if reviews else "testo_importato_da_validare")
        result.append({"id":act_id,"title":title,"link":url,"articles_indexed":n,
                       "official_documents":docs,"versions":versions,
                       "review":None if not reviews else dict(zip(("outcome","as_of","reviewer"),reviews)),
                       "status":flag})
    return {"as_of":as_of,"acts":len(result),"texts_present":sum(bool(x["official_documents"]) for x in result),
            "articles_indexed":sum(x["articles_indexed"] for x in result),
            "warning":"Non confondere il monitoraggio HTTP con la vigenza giuridica.",
            "records":result}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--db",default="app/neurolex.sqlite")
    p.add_argument("--as-of",default=date.today().isoformat())
    a=p.parse_args()
    db=connect(a.db)
    print(json.dumps(audit(db,a.as_of),ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
