#!/usr/bin/env python3
"""Critic normativo: audit preliminare di metadati e pertinenza, NON verifica giuridica automatica."""
import csv
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

TRUSTED = {
    "normattiva.it", "gazzettaufficiale.it", "eur-lex.europa.eu",
    "lavoro.gov.it", "inps.it", "inail.it", "agid.gov.it",
    "normelombardia.consiglio.regione.lombardia.it",
}
RELEVANCE = {"diretta", "condizionata", "complementare", "contesto", "non_pertinente"}
VALIDATION = {"verifica_articoli", "da_verificare", "verificato_articolo"}
SOURCE_TYPES = {"primaria", "istituzionale_secondaria", "non_istituzionale"}

def host_allowed(host):
    return host in TRUSTED or any(host.endswith("." + d) for d in TRUSTED)

def inspect(item):
    errors = []
    alerts = []
    for name in ["id", "titolo", "area", "url", "nota"]:
        if not item.get(name, "").strip():
            errors.append("campo_mancante:" + name)
    u = urlparse(item.get("url", ""))
    if u.scheme != "https" or not host_allowed(u.hostname or ""):
        errors.append("dominio_non_riconosciuto_o_url_non_https")
    if item.get("pertinenza_proposta") not in RELEVANCE:
        errors.append("pertinenza_non_classificata")
    if item.get("classe_fonte") not in SOURCE_TYPES:
        errors.append("classe_fonte_non_classificata")
    if item.get("verifica_testo") not in VALIDATION:
        errors.append("verifica_non_classificata")
    if u.path in ("", "/"):
        alerts.append("link_generico_sostituire_con_atto")
    if item.get("pertinenza_proposta") == "contesto":
        alerts.append("separare_dalle_tutele_direttamente_azionabili")
    if item.get("pertinenza_proposta") == "condizionata":
        alerts.append("identificare_destinatari_requisiti_territorio_tempi")
    if item.get("verifica_testo") != "verificato_articolo":
        alerts.append("vigenza_e_articoli_non_certificati")
    if item.get("classe_fonte") != "primaria":
        alerts.append("non_presentare_come_fonte_legislativa")
    # Una etichetta inserita dall'editor non e prova della pertinenza.
    return {
        "id": item.get("id"),
        "titolo": item.get("titolo"),
        "pertinenza_dichiarata": item.get("pertinenza_proposta"),
        "esito": "correggere_metadati" if errors else ("revisione_umana" if alerts else "pronto_per_verifica_esperta"),
        "errori": errors,
        "avvisi": alerts,
        "non_verificato_automaticamente": [
            "contenuto_integrale", "conferenza_semantica_con_il_quesito",
            "vigenza", "interpretazione", "applicabilita_individuale"
        ],
    }

def main():
    source = Path(sys.argv[1] if len(sys.argv) > 1 else "critic/fonti.csv")
    with source.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    out = [inspect(r) for r in rows]
    ids = [r.get("id", "") for r in rows]
    for result in out:
        if ids.count(result["id"]) > 1:
            result["errori"].append("id_duplicato")
            result["esito"] = "correggere_metadati"
    print(json.dumps({
        "tipo": "audit_preliminare_non_legale",
        "numero_fonti": len(rows),
        "esiti": {label: sum(r["esito"] == label for r in out)
                  for label in ["correggere_metadati", "revisione_umana", "pronto_per_verifica_esperta"]},
        "fonti": out,
    }, ensure_ascii=False, indent=2))
    return 2 if any(r["errori"] for r in out) else 0

if __name__ == "__main__":
    raise SystemExit(main())
