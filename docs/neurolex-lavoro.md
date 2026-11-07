# NeuroLex Lavoro — Specifica funzionale iniziale

## Obiettivo
Realizzare un'applicazione web accessibile per la ricerca delle disposizioni normative a tutela delle persone neurodivergenti e con disabilità nel lavoro, dal 1994 alla data corrente, includendo norme anteriori ancora rilevanti.

## Casi d'uso
- «Sono una persona autistica: quali tutele possono riguardare un colloquio di lavoro?»
- «Quali requisiti occorrono per accedere al collocamento mirato?»
- «Quali adattamenti posso chiedere nell'ambiente lavorativo?»
- «Quali obblighi si applicano all'impresa?»
- «Quale versione di una disposizione era vigente in una data specifica?»

## Moduli previsti
1. **Ricerca normativa:** parole chiave, ricerca semantica e domande in linguaggio naturale.
2. **Archivio versionato:** identificativi ufficiali, articoli, date, modifiche, abrogazioni e rinvii.
3. **Risposte assistite da IA (RAG):** recupero delle fonti prima della sintesi, con citazioni puntuali.
4. **Cronologia:** ricostruzione delle modifiche dal 1994 a oggi.
5. **Orientamento ai percorsi:** requisiti, servizi, procedure e principali limitazioni applicative.
6. **Area imprese:** collocamento mirato, selezioni accessibili, adattamenti e non discriminazione.
7. **Avvisi sugli aggiornamenti:** previo controllo delle nuove fonti ufficiali.

## Schema minimo dei dati per atto
- Identificativo univoco e tipo di atto
- Numero, data, titolo e autorità emanante
- Fonte ufficiale e URL permanente
- Pubblicazione ed entrata in vigore
- Articoli e commi pertinenti
- Versione temporale del testo, eventuali modifiche e abrogazioni
- Ambito: accesso, collocamento, selezione, permanenza, accomodamenti, discriminazione
- Destinatari e requisiti di applicazione
- Data dell'ultima verifica e revisore
- Stato di verifica: da controllare / verificato / da riesaminare

## Architettura proposta
- Frontend web responsive e progressive web app (valutazione da effettuare).
- Backend applicativo con API e gestione dei ruoli.
- Database relazionale, indicizzazione full-text e ricerca semantica.
- Ingestion di fonti ufficiali con tracciamento dei cambiamenti.
- RAG con citazioni, controllo della pertinenza e risposta «fonte insufficiente».
- Pannello di supervisione editoriale/giuridica.

## Requisiti trasversali
- WCAG 2.2 AA come obiettivo di progetto; test con utenti e tecnologie assistive.
- Interfacce a complessità regolabile, navigazione da tastiera, controllo degli stimoli e linguaggio chiaro.
- GDPR, minimizzazione dei dati e nessuna richiesta non necessaria di diagnosi o certificazioni.
- Distinzione fra informazione, orientamento e consulenza legale personalizzata.
- Nessuna affermazione di vigenza o diritto individuale senza fonte e controllo dei requisiti.

## Stato
Documento di specifica **preliminare**: non equivale a software sviluppato o validato.
