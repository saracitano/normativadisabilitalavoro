#!/usr/bin/env python3
"""Acquire specific official XML exports; never certify legal validity."""
import argparse, json, tempfile
from pathlib import Path
from urllib.request import build_opener, Request, HTTPRedirectHandler
from .legislation import connect
from .official_ingest import ingest, is_official_source

class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not is_official_source(newurl):
            raise ValueError("Untrusted redirect")
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def fetch_xml(url):
    if not is_official_source(url):
        raise ValueError("Untrusted origin")
    request=Request(url,headers={"Accept":"application/xml,text/xml",
        "User-Agent":"NeuroLex-Lavoro-Research/0.1"})
    with build_opener(SafeRedirect()).open(request,timeout=25) as response:
        if not is_official_source(response.url):
            raise ValueError("Untrusted redirect destination")
        kind=response.headers.get("Content-Type","").lower()
        raw=response.read(12_000_001)
        final_url=response.url
    if len(raw)>12_000_000:
        raise ValueError("File too large")
    upper=raw.upper()
    if b"<!DOCTYPE" in upper or b"<!ENTITY" in upper:
        raise ValueError("Unsupported DTD or XML entities")
    if "html" in kind or b"<html" in raw[:300].lower():
        raise ValueError("Export XML required; received HTML")
    text=raw.decode("utf-8-sig")
    if not text.lstrip().startswith("<"):
        raise ValueError("Not XML")
    return text, final_url

def main():
    p=argparse.ArgumentParser()
    p.add_argument("act_id")
    p.add_argument("--xml-url",required=True)
    p.add_argument("--publication-id",required=True)
    p.add_argument("--version",required=True)
    p.add_argument("--effective-as-of")
    p.add_argument("--db",default="app/neurolex.sqlite")
    a=p.parse_args()
    xml,url=fetch_xml(a.xml_url)
    with tempfile.TemporaryDirectory() as folder:
        path=Path(folder)/"source.xml"
        path.write_text(xml,encoding="utf-8")
        db=connect(a.db)
        result=ingest(db,a.act_id,path,a.publication_id,
                      a.version,a.effective_as_of,url)
        db.close()
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
