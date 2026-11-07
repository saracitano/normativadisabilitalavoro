# NeuroLex Lavoro — prima implementazione normativa

**Release sperimentale:** 2026-11-08. Non si tratta più del solo elenco: è disponibile un **database SQLite funzionante**, alimentato da schede articolo-per-articolo di due norme, con ricerca, ispezione del contenuto, gestione delle versioni integrali e provenienza dell'import.

## Implementato
- Legge 68/1999: **24 schede** (artt. 1–23, compreso 12-bis).
- D.Lgs. 216/2003: **9 schede** (artt. 1–7, compresi 4-bis e 5-bis).
- Indicizzazione per argomento, domande lessicali e filtri impliciti di rilevanza.
- Versioni integrali degli articoli importabili da file UTF-8 **solo con URL ufficiale, data del testo e impronta SHA-256**, consultabili dopo l'import.
- Avviso per art. 5-bis D.Lgs. 216/2003: la versione segnalata come efficace dal 01/01/2027 non deve essere mostrata come già vigente all'08/11/2026.

**Importante:** le schede in `seed.json` sono sintesi originali e riferimenti, **non testi normativi integrali**. Il campo `official_versions` resta vuoto fino all'import di un testo ufficiale controllato. Non è implementato un acquisitore automatico certificato da Normattiva; la data di efficacia delle versioni deve ancora essere validata da un giurista.

## Uso

Richiede Python 3.10+; nessuna dipendenza esterna.

```bash
python3 app/legislation.py init
python3 app/legislation.py search "accomodamenti ragionevoli"
python3 app/legislation.py show DLGS216-2003 3
python3 app/legislation.py show L68-1999 2
```

Dopo aver ottenuto dall'ente ufficiale il testo dell'articolo per la data corretta e averlo salvato in un file locale in UTF-8:

```bash
python3 app/legislation.py import-article L68-1999:2 /percorso/articolo2.txt --version-date 2026-11-08 --source-url "https://www.normattiva.it/..."
```

La versione è salvata in SQLite; `show` consente di visualizzarla. **L'import non certifica la correttezza del testo: `reviewed=0` fino a un futuro flusso di validazione.** Il database locale `app/neurolex.sqlite` è generato all'esecuzione e non è incluso nel repository.

## Fonti istituzionali
- [L. 68/1999 su Normattiva](https://www.normattiva.it/atto/caricaDettaglioAtto?atto.codiceRedazionale=099G0123&atto.dataPubblicazioneGazzetta=1999-03-23&tipoDettaglio=vigente)
- [D.Lgs. 216/2003 su Normattiva](https://www.normattiva.it/atto/caricaDettaglioAtto?atto.codiceRedazionale=003G0240&atto.dataPubblicazioneGazzetta=2003-08-13&tipoDettaglio=vigente)
- [Indice L. 68/1999 — MEF](https://def.finanze.it/DocTribFrontend/getAttoNormativoDetail.do?ACTION=getSommario&id=%7B472E7B20-E6D6-4339-87D5-994388357483%7D)
- [Indice D.Lgs. 216/2003 — MEF](https://def.finanze.it/DocTribFrontend/getAttoNormativoDetail.do?ACTION=getSommario&id=%7B644CDB48-95E2-4C09-A180-ED71F457EB58%7D)

## Prossime attività
1. Acquisizione sistematica dei testi consolidati ufficiali con versionamento per articolo.
2. Audit automatico su contenuto, data di vigenza e testi modificativi.
3. Estensione dell'archivio alle restanti fonti.
4. Interfaccia web e ricerca semantica RAG con prove testuali e controllo umano.

Non sono ancora disponibili un servizio web pubblico, acquisizione automatica, classificazione dei commi o un sistema capace di garantire vigenza ed esattezza.

## Estensione del corpus (8 novembre 2026)
Il file `seed.json` ora comprende **63 atti** del catalogo italiano, UE e della prima ricognizione regionale. Restano **33 schede di articoli** per le due norme pilota. Le altre 61 fonti sono registrate **solo a livello di atto**: la ricerca restituisce esplicitamente `status: solo_atto`; ciò non implica che il testo sia stato acquisito o che la vigenza sia stata controllata.

Il monitor tecnico è documentato in [monitor/README.md](../monitor/README.md). Le versioni integrate degli articoli restano da acquisire e validare prima dell'uso decisionale.
