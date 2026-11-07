# Acquisizione online di testi normativi ufficiali

Il programma [source_fetch.py](source_fetch.py) scarica XML da un URL istituzionale HTTPS indicato esplicitamente e lo trasferisce al sistema di importazione versionato. Non costruisce endpoint API inesistenti, non usa pagine HTML come testi normativi e non dichiara validato un testo importato.

```bash
python3 app/legislation.py init
python3 -m app.source_fetch L68-1999 --xml-url "URL_EXPORT_XML_UFFICIALE" --publication-id "099G0123" --version "VERSIONE_IDENTIFICATA"
python3 -m app.audit --as-of 2026-11-08
```

Il parametro opzionale `--effective-as-of` può essere compilato soltanto dopo verifica della data nei metadati ufficiali. Sono controllati dominio, reindirizzamento, dimensione, contenuto XML e hash; per la vigenza servono il testo consolidato con decorrenza e un controllo giuridico.

Fonti: [Open Data Normattiva](https://dati.normattiva.it/Come-scaricare-i-dati), [OpenAPI Normattiva](https://dati.normattiva.it/assets/come_fare_per/Normattiva%20OpenData.html), [EUR-Lex riuso dei contenuti](https://eur-lex.europa.eu/content/help/data-reuse/reuse-contents-eurlex-details.html?locale=it).

**Stato:** canale di acquisizione implementato, download e importazione massiva delle 63 norme ancora da eseguire e verificare.