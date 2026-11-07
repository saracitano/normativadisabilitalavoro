# Implementazione dei testi normativi: acquisizione, versioni e audit

Il catalogo contiene schede di atti, ma non deve essere confuso con il testo vigente. La pipeline `official_ingest.py` aggiunge la possibilità **reale** di acquisire documenti XML ufficiali in un database SQLite, conservando provenienza, contenuto originale, checksum, versione e articoli estratti.

## Dove trovare i testi
- [Normattiva Open Data](https://dati.normattiva.it/Come-scaricare-i-dati): documenti originari, vigenti, datati e multivigenti; API e specifiche pubblicate dal portale.
- [Normattiva — progetto](https://dati.normattiva.it/Il-progetto): significato delle versioni temporali.
- [EUR-Lex — riuso dei contenuti](https://eur-lex.europa.eu/content/help/data-reuse/reuse-contents-eurlex-details.html?locale=en): documenti in XML/Formex e servizi CELLAR.

**La pipeline attuale riceve file XML già acquisiti da canale ufficiale:** non tenta un download non documentato e non inventa endpoint API. Supporta l'estrazione euristica di elementi XML denominati `articolo` con numero; il contenuto è indicizzato solo come *non validato*. Altri formati (Formex UE, PDF, DOC) richiedono adattatori separati.

## Esempio d'uso
Dalla radice della repository, con Python 3.10+:

```bash
python3 app/legislation.py init
python3 -m app.official_ingest import-xml L68-1999 /percorso/atto-ufficiale.xml \
  --publication-id "099G0123" \
  --version "versione-scaricata-2026-11-08" \
  --effective-as-of "2026-11-08" \
  --origin-url "https://dati.normattiva.it/"
python3 -m app.audit --as-of 2026-11-08
```

La data `--effective-as-of` deve provenire dal documento/metadato ufficiale e **non** essere dedotta dal giorno di download. Se mancano dati affidabili, omettere il parametro: il file integrale viene archiviato, ma i testi non vengono associati a una data di efficacia.

## Revisione
La registrazione di una verifica giuridica richiede un revisore nominato, fonte, data e motivazione. `reviewed=0` per i testi importati; l'esistenza di una revisione non cambia automaticamente il campo `reviewed` né autorizza risposte senza controllare l'articolo esatto.

```bash
python3 -m app.official_ingest review L68-1999 --article 2 \
 --as-of 2026-11-08 --reviewer "revisore-giuridico" \
 --origin-url "https://www.normattiva.it/" --outcome incerto \
 --reason "Verifica della versione completa e degli atti modificativi ancora necessaria."
```

Non utilizzare l'esempio come una revisione effettivamente svolta.

## Prevenzione di errori
- Il sistema blocca la sovrascrittura silenziosa di due XML con lo stesso identificativo e versioni ma checksum differenti.
- Il sistema separa documenti acquisiti, articoli estratti, versioni e revisioni umane.
- Senza testo ufficiale e verifica, lo stato resta `non_implementato` o `testo_importato_da_validare`.
- Nessuna valutazione giuridica viene derivata dal semplice confronto tra hash di pagine web.
- La classificazione per articolo è euristica; deve essere verificata da persone competenti.
- Occorre rispettare limiti tecnici, condizioni di accesso e licenze delle fonti.

## Stato concreto (8 novembre 2026)
Il **codice di importazione, versione e audit è pubblicato**. Non sono ancora depositati nel repository XML di tutte le leggi, né è stata effettuata una validazione giuridica del corpus. La copertura è misurabile con `python3 -m app.audit` dopo l'inizializzazione.
