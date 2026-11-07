#!/usr/bin/env python3
"""NeuroLex: archivio normativo SQLite con articoli, versioni e ricerca; solo stdlib."""
import argparse, json, re, sqlite3, hashlib
from pathlib import Path
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS acts (
 id TEXT PRIMARY KEY, title TEXT NOT NULL, source_url TEXT NOT NULL, scope TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS articles (
 act_id TEXT NOT NULL, number TEXT NOT NULL, heading TEXT NOT NULL,
 explanation TEXT NOT NULL, keywords TEXT NOT NULL, relevance TEXT NOT NULL,
 review_status TEXT NOT NULL, warning TEXT NOT NULL DEFAULT '',
 PRIMARY KEY(act_id, number), FOREIGN KEY(act_id) REFERENCES acts(id));
CREATE TABLE IF NOT EXISTS official_versions (
 act_id TEXT NOT NULL, number TEXT NOT NULL, version_date TEXT NOT NULL,
 source_url TEXT NOT NULL, fetched_at TEXT NOT NULL,
 sha256 TEXT NOT NULL, text TEXT NOT NULL, reviewed INTEGER NOT NULL DEFAULT 0,
 PRIMARY KEY(act_id,number,version_date),
 FOREIGN KEY(act_id,number) REFERENCES articles(act_id,number));
"""

def connect(path):
    db=sqlite3.connect(path)
    db.execute("PRAGMA foreign_keys=ON")
    db.executescript(SCHEMA)
    return db

def bootstrap(db, seed):
    data=json.loads(Path(seed).read_text(encoding="utf-8"))
    with db:
        for a in data["acts"]:
            db.execute("INSERT OR REPLACE INTO acts VALUES (?,?,?,?)",
                       (a["id"],a["title"],a["source_url"],a["scope"]))
            for v in a["articles"]:
                db.execute("""INSERT OR REPLACE INTO articles
                    (act_id,number,heading,explanation,keywords,relevance,review_status,warning)
                    VALUES (?,?,?,?,?,?,?,?)""",
                    (a["id"],v["number"],v["heading"],v["explanation"],v["keywords"],
                     v["relevance"],v["status"],v.get("future_effect_warning","")))

def add_official(db, path, metadata, version_date, source_url):
    """Importa un testo da file controllato da un operatore, senza fingere di averlo scaricato."""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", version_date):
        raise ValueError("version_date deve essere YYYY-MM-DD")
    if not source_url.startswith("https://"):
        raise ValueError("Inserire URL HTTPS della fonte ufficiale")
    text=Path(path).read_text(encoding="utf-8").strip()
    if len(text)<30:
        raise ValueError("Testo troppo breve per una versione di articolo")
    act,number=metadata.split(":",1)
    now=datetime.now(timezone.utc).isoformat()
    sha=hashlib.sha256(text.encode()).hexdigest()
    with db:
        db.execute("""INSERT OR REPLACE INTO official_versions
                   (act_id,number,version_date,source_url,fetched_at,sha256,text,reviewed)
                   VALUES (?,?,?,?,?,?,?,0)""",
                   (act,number,version_date,source_url,now,sha,text))
    return {"article":metadata,"date":version_date,"sha256":sha,"reviewed":False}

def search(db, terms, with_text=False):
    tokens=[v.casefold() for v in re.findall(r"[^\W_]+", terms, re.UNICODE)]
    if not tokens: return []
    query="""SELECT a.act_id,a.number,a.heading,a.explanation,a.keywords,a.relevance,
                    a.review_status,a.warning,t.title,t.source_url,
                    (SELECT COUNT(*) FROM official_versions v WHERE v.act_id=a.act_id AND v.number=a.number) versions
             FROM articles a JOIN acts t ON t.id=a.act_id"""
    rows=[]
    for r in db.execute(query).fetchall():
        hay=(" ".join(str(v) for v in r[2:5])).casefold()
        score=sum(3 if token in str(r[2]).casefold() else 2 if token in str(r[4]).casefold() else 1 if token in hay else 0 for token in tokens)
        if score:
            rows.append({"act_id":r[0],"article":r[1],"title":r[2],"summary":r[3],
                "relevance":r[5],"review_status":r[6],"warning":r[7],
                "act_title":r[8],"source_url":r[9],"official_versions":r[10],
                "score":score,"status":"testo_importato" if r[10] else "solo_scheda"})
    return sorted(rows,key=lambda x:(-x["score"],x["act_id"],x["article"]))

def main():
    p=argparse.ArgumentParser(description="Archivio NeuroLex: schede + importazione versioni integrali")
    p.add_argument("--db",default="app/neurolex.sqlite")
    sub=p.add_subparsers(dest="command",required=True)
    x=sub.add_parser("init"); x.add_argument("--seed",default="app/seed.json")
    x=sub.add_parser("search");x.add_argument("text")
    x=sub.add_parser("show");x.add_argument("act");x.add_argument("article")
    x=sub.add_parser("import-article");x.add_argument("act_article",
        help="esempio L68-1999:1");x.add_argument("file");x.add_argument("--version-date",required=True);x.add_argument("--source-url",required=True)
    args=p.parse_args()
    Path(args.db).parent.mkdir(parents=True,exist_ok=True)
    db=connect(args.db)
    if args.command=="init":
        bootstrap(db,args.seed)
        print(json.dumps({"acts":db.execute("select count(*) from acts").fetchone()[0],
            "articles":db.execute("select count(*) from articles").fetchone()[0],
            "official_texts":db.execute("select count(*) from official_versions").fetchone()[0]}))
    elif args.command=="search":
        print(json.dumps(search(db,args.text),ensure_ascii=False,indent=2))
    elif args.command=="show":
        item=db.execute("""SELECT a.heading,a.explanation,a.review_status,a.warning,t.source_url
                  FROM articles a JOIN acts t ON a.act_id=t.id WHERE a.act_id=? AND a.number=?""",
                  (args.act,args.article)).fetchone()
        if not item: raise SystemExit("Articolo non presente")
        versions=db.execute("""SELECT version_date,source_url,sha256,reviewed,text FROM official_versions
                             WHERE act_id=? AND number=? ORDER BY version_date DESC""",
                             (args.act,args.article)).fetchall()
        print(json.dumps({"heading":item[0],"explanation":item[1],"status":item[2],
             "warning":item[3],"normattiva_url":item[4],"versions":[dict(zip(
             ["version_date","source_url","sha256","reviewed","text"],x)) for x in versions]},
             ensure_ascii=False,indent=2))
    elif args.command=="import-article":
        print(json.dumps(add_official(db,args.file,args.act_article,args.version_date,args.source_url),ensure_ascii=False))
    db.close()

if __name__=="__main__": main()
