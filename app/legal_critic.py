#!/usr/bin/env python3
"""Critic sulla pertinenza degli articoli IMPORTATI, con blocco vigenza.

Evidenza documentale, non parere legale. Senza versione importata e revisione
umana applicabile non restituisce mai una norma come 'vigente verificata'.
"""
import argparse
import json
import re
from datetime import date
from .legislation import connect
from .official_ingest import SCHEMA

def tokens(value):
    stop={"di","a","da","in","con","su","per","il","lo","la","i","gli","le",
          "un","una","e","ed","o","che","sono","quali","come","del","della"}
    return [t for t in re.findall(r"[^\W_]+",value.casefold(),re.UNICODE)
            if len(t)>2 and t not in stop]

def latest_review(db, act, article, as_of):
    # Review must concern this article and this temporal cut; generic act review
    # must not be promoted as article-specific verification.
    return db.execute("""SELECT outcome,as_of,reviewer,official_url,justification
           FROM legal_reviews WHERE act_id=? AND article=? AND as_of=?
           ORDER BY review_date DESC LIMIT 1""",(act,article,as_of)).fetchone()

def evaluate(db, query, as_of, limit=25):
    db.executescript(SCHEMA)
    words=tokens(query)
    if not words: return []
    rows=db.execute("""SELECT v.act_id,v.number,v.version_date,v.source_url,v.text,
                            v.sha256,a.heading,a.explanation,t.title
                       FROM official_versions v
                       JOIN articles a ON a.act_id=v.act_id AND a.number=v.number
                       JOIN acts t ON t.id=v.act_id
                       WHERE v.version_date=(
                          SELECT MAX(v2.version_date) FROM official_versions v2
                          WHERE v2.act_id=v.act_id AND v2.number=v.number
                                AND v2.version_date<=?
                       )""",(as_of,)).fetchall()
    result=[]
    for act,article,version_date,url,body,sha,heading,explanation,title in rows:
        sections=re.split(r"(?<=[.;])\s+",body)
        ranked=[]
        for s in sections:
            score=sum(1 for word in words if word in s.casefold())
            if score: ranked.append((score,s))
        if not ranked:continue
        ranked.sort(key=lambda x:-x[0])
        evidence=" ".join(x[1] for x in ranked[:2])[:500]
        review=latest_review(db,act,article,as_of)
        validated=False  # A review must be cryptographically tied to this exact version before any automatic certification
        result.append({
          "act_id":act,"article":article,"act_title":title,"heading":heading,
          "as_of":as_of,"imported_version_date":version_date,
          "source_url":url,"document_sha256":sha,"evidence_excerpt":evidence,
          "relevance_score_lexical":sum(x[0] for x in ranked[:2]),
          "legal_status":"non_certificato",
          "review":None if not review else {"outcome":review[0],"as_of":review[1],
                                        "reviewer":review[2],"source_url":review[3]},
          "warning":"La corrispondenza lessicale non prova conferenza o applicabilita; lo stato giuridico non e certificato. Il riesame non e ancora legato all hash della versione."
        })
    result.sort(key=lambda x:-x["relevance_score_lexical"])
    return result[:limit]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("question")
    p.add_argument("--db",default="app/neurolex.sqlite")
    p.add_argument("--as-of",default=date.today().isoformat())
    p.add_argument("--limit",type=int,default=25)
    a=p.parse_args()
    db=connect(a.db)
    print(json.dumps({"question":a.question,"as_of":a.as_of,
       "results":evaluate(db,a.question,a.as_of,a.limit),
       "notice":"Nessun esito e' una consulenza legale; senza revisione non certificare la vigenza."},
       ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
