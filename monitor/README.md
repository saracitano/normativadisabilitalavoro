# Monitor automatico e controllo della vigenza — NeuroLex Lavoro

Il monitor effettua un **controllo tecnico** degli URL ufficiali associati agli atti censiti. Esegue richieste HTTPS, normalizza parzialmente i testi delle pagine e confronta le impronte SHA-256 con quelle del controllo precedente.

## Stati
- `baseline_created`: prima acquisizione dell'impronta, non verifica giuridica.
- `no_page_change_detected`: impronta invariata; **non prova che la norma sia vigente**.
- `possible_change_review_required`: variazione della pagina; **non prova una modifica legislativa**.
- `source_unreachable`: errore di rete/portale; non equivale ad abrogazione.
- `insufficient_permalink`: link troppo generico per monitorare un atto.
- `deferred`: non controllato per limite impostato.

## Esecuzione
```bash
python3 monitor/monitor.py
python3 -m unittest discover -s tests
```

I risultati vengono scritti in `monitor/state.json` e `monitor/latest-report.json`. Lo stato precedente viene conservato se una fonte non è raggiungibile.

## Aggiornamento periodico
Il workflow GitHub Actions in `.github/workflows/check-normativa.yml` è programmato ogni lunedì e può essere avviato manualmente da Actions, **se GitHub Actions è abilitato e i permessi del repository lo consentono**. Registra lo stato e il report tramite commit. Un commit del monitor attesta solo l'esito della verifica tecnica.

## Stato di validazione giuridica
**Non implementato automaticamente.** Per confermare vigenza di legge e commi servono acquisizione del testo consolidato a una precisa data, confronto tra versioni, identificazione di atti modificativi, efficacia differita e regimi transitori. Il lavoro richiede fonti ufficiali e revisione umana qualificata.

## Per rendere il controllo più affidabile
1. Sostituire i link generici con URL ELI o atti ufficiali puntuali.
2. Integrare metadati strutturati sulle modifiche e relative decorrenze.
3. Alimentare `official_versions` dell'archivio SQLite.
4. Collegare il Critic per verificare **articolo e comma** prima di dichiarare una tutela vigente.
5. Sviluppare alert a un revisore su modifiche effettive e divergenze; non promuovere automaticamente una disposizione a «verificata».

**Dati non pubblicati:** diagnosi, documenti clinici, dati personali. Nessuna fonte di terzi viene ripubblicata integralmente in automatico.
