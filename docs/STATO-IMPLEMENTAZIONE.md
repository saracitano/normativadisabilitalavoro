# Stato verificabile dell'implementazione — 8 novembre 2026

Questo documento distingue **codice esistente**, **dati realmente importati** e **verifiche giuridiche ancora mancanti**. Non afferma che l'intero archivio legislativo sia stato acquisito.

## Situazione iniziale del database distribuito
- Atti censiti nel seed: **63**.
- Atti con schede per articolo: **2** (Legge 68/1999 e D.Lgs. 216/2003).
- Schede di articoli: **33**.
- Atti aggiuntivi senza articolato completo: **61**.
- Documenti ufficiali XML distribuiti nel repository: **0**.
- Versioni normative integrali verificate nel repository: **0**.
- Revisioni giuridiche qualificate registrate nel repository: **0**.

Questi valori si riferiscono ai materiali **pubblicati nel repository**, non a eventuali database locali di singoli utilizzatori. Il file SQLite viene generato localmente, non pubblicato.

## Funzioni software
| Funzione | Stato |
|---|---|
| Registro di atti e schede riassuntive | Implementato |
| Ricerca lessicale degli atti e schede | Implementata |
| Importazione XML da file locale ufficiale | Codice implementato, da verificare su XML reali Normattiva |
| Scaricamento XML da URL HTTPS ufficiale puntuale | Codice implementato, richiede URL diretto e collaudo con fonti reali |
| Salvataggio documento originale con hash | Codice implementato |
| Estrazione euristica di articoli XML | Codice implementato, non validato per tutti i formati |
| Versionamento per data esplicita | Codice implementato, data da fonte ufficiale obbligatoria |
| Critic con estratti documentali | Implementato per testi importati, non certifica vigenza |
| Monitor del cambiamento delle pagine | Configurato, non sostituisce verifica di modifiche legislative |
| Test automatici Python GitHub Actions | Workflow configurato: esito esecuzione da controllare su Actions |
| Acquisizione sistematica dell'intero corpus | **Non completata** |
| Accertamento giuridico di vigenza articolo/comma | **Non completato** |
| Analisi di articoli modificativi e abrogazioni | **Non completata** |
| Adattatori EUR-Lex/Formex e raccolta regionale | **Non completati** |
| Applicazione web per utenti finali | **Non completata** |

## Funzionamento della pipeline
1. La fonte viene censita nel catalogo.
2. Il sistema richiede un documento ufficiale in XML e l'identificazione della versione; per download serve un **URL diretto reale**, non la homepage.
3. Il file originale è archiviato con SHA-256, URL, identificativo e data.
4. Gli articoli sono estratti e registrati **come non validati**.
5. Il Critic cerca nei testi importati e mostra estratti e riferimenti; la conferenza giuridica deve essere verificata.
6. Il revisore esamina articoli, disposizioni temporali e collegamenti modificativi.
7. Solo in seguito a un controllo umano sul testo specifico sarà possibile pubblicare uno stato giuridico verificato.
8. Il monitor settimanale segnala potenziali modifiche, ma **non deduce un'abrogazione da un errore HTTP o una modifica da un hash differente**.

## Fonti tecniche ufficiali per l'acquisizione
- [Normattiva Open Data — come scaricare i dati](https://dati.normattiva.it/Come-scaricare-i-dati)
- [Specifica delle API Normattiva Open Data](https://dati.normattiva.it/assets/come_fare_per/Normattiva%20OpenData.html)
- [Riuso dei contenuti EUR-Lex](https://eur-lex.europa.eu/content/help/data-reuse/reuse-contents-eurlex-details.html?locale=en)

Normattiva documenta collezioni in XML, JSON, AKN, HTML e altri formati, con metadati di vigenza; alcune collezioni prevedono richiesta e conferma tramite email. Non presumere che una API consenta download anonimi senza consultare la specifica di accesso. EUR-Lex offre strumenti di download e Cellar; alcuni servizi richiedono registrazione.

## Regola non negoziabile
**Non è ammesso rispondere “diritto vigente” sulla base di una sola scheda, di un collegamento HTTP funzionante, di un testo non verificato o di una versione con data futura.** La qualità scientifica e la tracciabilità prevalgono sull'apparente completezza del database.

## Collaudo
Dalla radice del repository:
```bash
python3 -m unittest discover -s tests -v
python3 app/legislation.py init
python3 -m app.audit --as-of 2026-11-08
python3 -m app.legal_critic "accomodamenti ragionevoli" --as-of 2026-11-08
```
Fino a quando non sono stati importati testi ufficiali, l'ultima query non deve restituire articoli sostenuti da testo integrale.
