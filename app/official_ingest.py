#!/usr/bin/env python3
"""Ingestione controllata di testi normativi XML ufficiali; nessuna vigenza presunta.

Accetta un file XML Normattiva/NIR acquisito tramite i canali Open Data.
Conserva documento integrale e metadati di provenienza; estrazione articoli
best-effort in modo NON verificato. Non inventa commi o date di efficacia.
"""
import argparse
import hashlib
import json
import re
import sqlite3
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from .legislation import connect

SCHEMA = """
CREATE TABLE IF NOT EXISTS official_documents (
 act_id TEXT NOT NULL,
 publication_id TEXT NOT NULL,
 version_label TEXT NOT NULL,
 effective_as_of TEXT,
 origin_url TEXT NOT NULL,
 acquired_at TEXT NOT NULL,
 sha256 TEXT NOT NULL,
 payload TEXT NOT NULL,
 content_type TEXT NOT NULL,
 review_status TEXT NOT NULL DEFAULT 'importato_non_validato',
 PRIMARY KEY(act_id, publication_id, version_label),
 FOREIGN KEY(act_id) REFERENCES acts(id)
);
CREATE TABLE IF NOT EXISTS legal_reviews (
 act_id TEXT NOT NULL,
 article TEXT,
 review_date TEXT NOT NULL,
 as_of TEXT NOT NULL,
 reviewer TEXT NOT NULL,
 official_url TEXT NOT NULL,
 outcome TEXT NOT NULL,
 justification TEXT NOT NULL,
 PRIMARY KEY(act_id, article, review_date, as_of)
);
"""
TRUSTED_DOMAINS = (
    "normattiva.it", "gazzettaufficiale.it", "dati.normattiva.it",
    "eur-lex.europa.eu", "lavoro.gov.it", "inail.it", "inps.it",
    "parlamento.it", "agid.gov.it", "def.finanze.it"
)

def is_official_source(url):
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    return (parsed.scheme == "https" and
            any(host == domain or host.endswith("." + domain)
                for domain in TRUSTED_DOMAINS))

VALID_OUTCOMES = {"vigente_verificato","non_vigente_verificato","efficacia_futura","incerto","fonte_non_pertinente"}

def local(tag):
    return tag.rsplit("}", 1)[-1].lower()

def parse_xml(xmltext):
    root = ET.fromstring(xmltext)
    # NIR/OpenData may have different namespaces and hierarchies.
    # Extract only elements explicitly named articolo, not paragraphs/note.
    articles=[]
    for el in root.iter():
        if local(el.tag) != "articolo":
            continue
        number = next((" ".join("".join(ch.itertext()).split()) for ch in el
                       if local(ch.tag) in {"num", "numero"}), "")
        if not number:
            continue
        found=re.search(r"\d+(?:[- ]?(?:bis|ter|quater))?",number.lower())
        if not found: continue
        key=found.group(0).replace(" ","-")
        body=" ".join(" ".join(el.itertext()).split())
        if len(body) >= 30:
            articles.append((key,body))
    return articles

def ingest(db, act, xml_file, publication_id, version_label, effective_as_of, origin_url):
    if not is_official_source(origin_url):
        raise ValueError("L'URL deve essere HTTPS")
    if not publication_id or not version_label:
        raise ValueError("Servono identificativo documento e versione")
    if effective_as_of:
        datetime.strptime(effective_as_of,"%Y-%m-%d")
    payload=Path(xml_file).read_text(encoding="utf-8")
    parts=parse_xml(payload)  # fail on malformed XML; no partial writes
    digest=hashlib.sha256(payload.encode("utf-8")).hexdigest()
    ts=datetime.now(timezone.utc).isoformat()
    with db:
        db.executescript(SCHEMA)
        if not db.execute("SELECT 1 FROM acts WHERE id=?",(act,)).fetchone():
            raise ValueError("Atto non presente in archivio; importare prima il catalogo")
        old=db.execute("""SELECT sha256 FROM official_documents
                       WHERE act_id=? AND publication_id=? AND version_label=?""",
                       (act,publication_id,version_label)).fetchone()
        if old and old[0]!=digest:
            raise ValueError("Versione gia' registrata con hash diverso: non sovrascrivere; indagare")
        db.execute("""INSERT OR IGNORE INTO official_documents
                     (act_id,publication_id,version_label,effective_as_of,origin_url,
                      acquired_at,sha256,payload,content_type)
                     VALUES (?,?,?,?,?,?,?,?,?)""",
                   (act,publication_id,version_label,effective_as_of,origin_url,
                    ts,digest,payload,"application/xml"))
        for number,body in parts:
            known=db.execute("SELECT 1 FROM articles WHERE act_id=? AND number=?",
                             (act,number)).fetchone()
            if not known:
                db.execute("""INSERT INTO articles
                   (act_id,number,heading,explanation,keywords,relevance,review_status,warning)
                   VALUES (?,?,?,?,?,?,?,?)""",
                   (act,number,"Articolo "+number,
                    "Testo importato; analisi giuridica non ancora validata.",
                    "", "da_esaminare", "testo_da_validare",
                    "Verificare manualmente classificazione, versione e decorrenza"))
            if effective_as_of:
                prev=db.execute("""SELECT sha256 FROM official_versions
                         WHERE act_id=? AND number=? AND version_date=?""",
                         (act,number,effective_as_of)).fetchone()
                hashtext=hashlib.sha256(body.encode("utf-8")).hexdigest()
                if prev and prev[0]!=hashtext:
                    raise ValueError("Testo articolo confliggente con una versione preesistente")
                db.execute("""INSERT OR IGNORE INTO official_versions
                          (act_id,number,version_date,source_url,fetched_at,sha256,text,reviewed)
                          VALUES (?,?,?,?,?,?,?,0)""",
                          (act,number,effective_as_of,origin_url,ts,hashtext,body))
    return {"act":act,"publication_id":publication_id,"version":version_label,
            "sha256":digest,"articles_extracted":len(parts),
            "stored_article_versions":len(parts) if effective_as_of else 0,
            "legal_review":"non_effettuata"}

def review(db, act, article, as_of, reviewer, official_url, outcome, justification):
    if outcome not in VALID_OUTCOMES: raise ValueError("Esito non valido")
    if not all((as_of,reviewer,official_url,justification)): raise ValueError("Metadati di revisione incompleti")
    datetime.strptime(as_of,"%Y-%m-%d")
    if len(justification)<30: raise ValueError("Motivazione insufficiente")
    if not is_official_source(official_url): raise ValueError("Serve una fonte istituzionale HTTPS riconosciuta")
    with db:
        db.executescript(SCHEMA)
        if article and not db.execute("SELECT 1 FROM articles WHERE act_id=? AND number=?",(act,article)).fetchone():
            raise ValueError("Articolo sconosciuto")
        if not db.execute("SELECT 1 FROM official_documents WHERE act_id=?",(act,)).fetchone():
            raise ValueError("Non e' presente un documento ufficiale importato")
        when=datetime.now(timezone.utc).isoformat()
        db.execute("""INSERT INTO legal_reviews
                     (act_id,article,review_date,as_of,reviewer,official_url,outcome,justification)
                     VALUES (?,?,?,?,?,?,?,?)""",
                     (act,article,when,as_of,reviewer,official_url,outcome,justification))
    return {"act":act,"article":article,"as_of":as_of,"outcome":outcome,"reviewed_by":reviewer}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--db",default="app/neurolex.sqlite")
    sub=p.add_subparsers(dest="cmd",required=True)
    x=sub.add_parser("import-xml")
    x.add_argument("act");x.add_argument("file");x.add_argument("--publication-id",required=True)
    x.add_argument("--version",required=True);x.add_argument("--effective-as-of")
    x.add_argument("--origin-url",required=True)
    x=sub.add_parser("review")
    x.add_argument("act");x.add_argument("--article")
    x.add_argument("--as-of",required=True);x.add_argument("--reviewer",required=True)
    x.add_argument("--origin-url",required=True);x.add_argument("--outcome",required=True,
      choices=sorted(VALID_OUTCOMES));x.add_argument("--reason",required=True)
    a=p.parse_args()
    db=connect(a.db)
    if a.cmd=="import-xml":
        result=ingest(db,a.act,a.file,a.publication_id,a.version,a.effective_as_of,a.origin_url)
    else:
        result=review(db,a.act,a.article,a.as_of,a.reviewer,a.origin_url,a.outcome,a.reason)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
