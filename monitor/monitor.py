#!/usr/bin/env python3
"""Monitora cambiamenti in pagine ufficiali. NON certifica la vigenza delle norme."""
import argparse
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.bits = []
        self.hidden = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "svg", "noscript"):
            self.hidden += 1
    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg", "noscript") and self.hidden:
            self.hidden -= 1
    def handle_data(self, data):
        if not self.hidden:
            self.bits.append(data)

def trusted(url):
    h = (urlparse(url).hostname or "").lower()
    domains = (
        "normattiva.it", "gazzettaufficiale.it", "eur-lex.europa.eu",
        "lavoro.gov.it", "inail.it", "inps.it",
        "normelombardia.consiglio.regione.lombardia.it",
    )
    return urlparse(url).scheme == "https" and any(
        h == x or h.endswith("." + x) for x in domains
    )

def fingerprint(url):
    req = Request(url, headers={"User-Agent": "NeuroLex-Lavoro-Research-Monitor/0.1 (non-commercial)", "Accept": "text/html,text/plain,application/xhtml+xml"})
    with urlopen(req, timeout=25) as resp:
        raw = resp.read(2_000_000)
        kind = resp.headers.get("Content-Type", "").lower()
        charset = resp.headers.get_content_charset() or "utf-8"
        last_modified = resp.headers.get("Last-Modified")
        etag = resp.headers.get("ETag")
        status = resp.status
    if "html" in kind or raw.lstrip().startswith(b"<"):
        parser = VisibleText()
        parser.feed(raw.decode(charset, errors="replace"))
        cleaned = " ".join(" ".join(parser.bits).split())
    else:
        cleaned = raw.decode(charset, errors="replace")
        cleaned = re.sub(r"\s+", " ", cleaned)
    # A web page can contain dynamic elements, so a hash difference is a
    # *possible page change*, never proof of a legislative amendment.
    return {"status_code": status, "sha256": hashlib.sha256(cleaned.encode()).hexdigest(),
            "etag": etag, "last_modified": last_modified, "size": len(cleaned)}

def run(seed_path, state_path, report_path, limit=100):
    seed = json.loads(Path(seed_path).read_text(encoding="utf-8"))
    old = json.loads(Path(state_path).read_text(encoding="utf-8")) if Path(state_path).exists() else {}
    old_records = old.get("records", {})
    current_records = dict(old_records)
    now = datetime.now(timezone.utc).isoformat()
    events = []
    checked = 0
    skipped = 0
    for act in seed["acts"]:
        identifier = act["id"]
        url = act["source_url"]
        if not trusted(url) or urlparse(url).path in ("", "/"):
            skipped += 1
            events.append({"id": identifier, "result": "insufficient_permalink",
                           "note": "URL non specifico: servono ELI, permalink o riferimento atto."})
            continue
        if checked >= limit:
            events.append({"id": identifier, "result": "deferred", "note": "Limite di controllo raggiunto."})
            continue
        checked += 1
        try:
            fresh = fingerprint(url)
            prior = old_records.get(identifier)
            changed = prior and prior.get("sha256") != fresh["sha256"]
            result = "possible_change_review_required" if changed else ("no_page_change_detected" if prior else "baseline_created")
            current_records[identifier] = {"url": url, "checked_at": now, **fresh}
            events.append({"id": identifier, "result": result,
                           "note": "Impronta pagina: NON certifica vigenza o contenuto dell'atto."})
        except Exception as exc:
            # Do not overwrite the last successful fingerprint on network errors.
            events.append({"id": identifier, "result": "source_unreachable",
                           "note": str(exc)[:180]})
        time.sleep(0.15)
    state = {"last_run_at": now, "records": current_records,
             "disclaimer": "Esiti tecnici, non certificazione del testo vigente."}
    Path(state_path).parent.mkdir(parents=True,exist_ok=True)
    Path(state_path).write_text(json.dumps(state,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    counts = {}
    for event in events:
        counts[event["result"]] = counts.get(event["result"], 0) + 1
    report = {
        "generated_at": now,
        "acts_in_catalogue": len(seed["acts"]),
        "urls_checked": checked,
        "generic_urls_skipped": skipped,
        "results": counts,
        "events": events,
        "legal_validation": False,
        "legal_qualification": "Controllo tecnico di raggiungibilità e possibili cambiamenti; revisione giuridica obbligatoria."
    }
    Path(report_path).parent.mkdir(parents=True,exist_ok=True)
    Path(report_path).write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--seed",default="app/seed.json")
    p.add_argument("--state",default="monitor/state.json")
    p.add_argument("--report",default="monitor/latest-report.json")
    p.add_argument("--limit",type=int,default=100)
    args=p.parse_args()
    r=run(args.seed,args.state,args.report,args.limit)
    print(json.dumps({"time":r["generated_at"],"counts":r["results"],
                      "legal_validation":False},ensure_ascii=False))

if __name__=="__main__":
    main()
