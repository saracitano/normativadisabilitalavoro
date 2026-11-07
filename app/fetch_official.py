#!/usr/bin/env python3
"""Acquisizione di XML ufficiali da URL esatti, senza endpoint inventati.

L'utente/revisore fornisce un URL diretto ufficiale all'XML; non effettua
ricerche generiche né dichiara in automatico la vigenza giuridica.
"""
import argparse
import ipaddress
import json
import socket
import tempfile
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler
from .official_ingest import is_official_source, ingest
from .legislation import connect

MAX_BYTES = 8_000_000

def ensure_public_dns(host):
    if not host:
        raise ValueError("Host assente")
    for answer in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM):
        address = ipaddress.ip_address(answer[4][0])
        if not address.is_global:
            raise ValueError("Indirizzo di rete non pubblico: " + str(address))

class OfficialRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not is_official_source(newurl):
            raise ValueError("Redirect verso dominio non istituzionale")
        ensure_public_dns(urlparse(newurl).hostname)
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def download_xml(url):
    if not is_official_source(url):
        raise ValueError("URL fuori dagli host istituzionali consentiti")
    ensure_public_dns(urlparse(url).hostname)
    opener = build_opener(OfficialRedirect())
    request=Request(url, headers={
        "Accept":"application/xml,text/xml,application/akn+xml,application/octet-stream",
        "User-Agent":"NeuroLex-Lavoro-Acquisition/0.1"
    })
    with opener.open(request,timeout=30) as response:
        if not is_official_source(response.geturl()):
            raise ValueError("URL finale fuori dagli host consentiti")
        payload=response.read(MAX_BYTES+1)
        if len(payload)>MAX_BYTES:
            raise ValueError("XML supera il limite dimensionale")
        if payload.lstrip()[:1]!=b"<":
            raise ValueError("La risorsa non sembra contenere XML")
        return payload.decode("utf-8-sig")

def main():
    p=argparse.ArgumentParser(description="Importa un XML puntuale da fonte ufficiale")
    p.add_argument("act")
    p.add_argument("--xml-url",required=True)
    p.add_argument("--publication-id",required=True)
    p.add_argument("--version",required=True)
    p.add_argument("--effective-as-of")
    p.add_argument("--db",default="app/neurolex.sqlite")
    args=p.parse_args()
    xml=download_xml(args.xml_url)
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp)/"official.xml"
        path.write_text(xml,encoding="utf-8")
        db=connect(args.db)
        try:
            result=ingest(db,args.act,path,args.publication_id,args.version,
                          args.effective_as_of,args.xml_url)
        finally:
            db.close()
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
