# MASTERFILE — Neurodivergenza Diversità al lavoro
> **Documento canonico di continuità del progetto** · Versione 1.3 · Revisione: **16 novembre 2026** · Repository: [saracitano/normativadisabilitalavoro](https://github.com/saracitano/normativadisabilitalavoro) · Branch: `main`.
>
> **All'avvio di una nuova chat:** fornire questo URL e chiedere di leggere integralmente `MASTERFILE.md`, `README.md`, l'audit JSON e i file pertinenti prima di apportare modifiche. Il contenuto del masterfile è una *istantanea versionata*; non sostituisce la verifica degli ultimi commit.

## 0. Principio di continuità e fonte di verità
Il repository GitHub **è il riferimento persistente** del progetto. Questo file è la **mappa principale del patrimonio conoscitivo pubblicabile**: conserva le decisioni, collega la documentazione dettagliata e distingue fatti, ipotesi, codice e verifiche. Non pretende di riprodurre ogni conversazione né contiene dati privati, dataset o manoscritti inediti.

**Regola delle fonti:** per lo stato di un componente prevalgono il codice e i file di dati presenti nell'ultimo commit su `main`; per una norma prevale sempre il **testo istituzionale applicabile alla data richiesta**, verificato e documentato. Una spiegazione scritta in chat o nel masterfile non certifica mai la vigenza.

### Identità
- **Titolo scientifico:** *Neurodivergenza Diversità al lavoro*.
- **Applicazione progettata:** *NeuroLex Lavoro*.
- **Problema:** frammentazione e complessità delle informazioni normative sull'accesso e la permanenza nel lavoro delle persone neurodivergenti e con disabilità.
- **Obiettivo:** un'infrastruttura accessibile, scientificamente fondata, giuridicamente tracciabile, utile a persone, servizi di orientamento, enti del Terzo settore, imprese e professionisti HR.
- **Perimetro cronologico:** 1994–oggi, **includendo norme anteriori tuttora pertinenti**.
- **Perimetro giuridico:** Italia, Unione europea, convenzioni internazionali e successivamente fonti regionali/attuative e giurisprudenza.
- **Lingua di lavoro:** italiano. Documentazione scientifica con bibliografia verificata.

## 1. Patrimonio scientifico consolidato
Il progetto si fonda su una convergenza di:
- **Pedagogia speciale, pedagogia della disabilità e approccio inclusivo:** barriere e facilitatori, partecipazione, personalizzazione, progetto di vita e autonomia.
- **Modello biopsicosociale e approccio dei diritti:** la disabilità non va ridotta alla diagnosi; contano condizioni ambientali, organizzative e relazionali.
- **Neurodiversità e transizione al lavoro:** rispetto della pluralità di funzionamenti, sostegni proporzionati, orientamento e adattamento dei contesti.
- **Disability studies, lavoro e non discriminazione:** accomodamenti ragionevoli, accessibilità dei processi di selezione, mantenimento dell'occupazione, collocamento mirato.
- **Progettazione universale, accessibilità cognitiva, co-design:** interfacce comprensibili, navigazione semplice, controllo degli stimoli, test con utenti diversi.
- **IA e affidabilità giuridica:** retrieval da fonti autorevoli, citazioni puntuali, data di efficacia, tracciamento delle versioni, segnalazione di lacune e supervisione umana.

**Distinzione indispensabile:** neurodivergenza, diagnosi (ad esempio autismo/ADHD/DSA), disabilità riconosciuta, invalidità civile e requisiti del collocamento mirato **non sono automaticamente equivalenti**. Ogni beneficio deve essere collegato alla propria disciplina.

### Domande di ricerca e sviluppo
1. Come ridurre le barriere di accesso e comprensione del diritto del lavoro per le persone neurodivergenti?
2. Un sistema informativo tracciabile può sostenere autodeterminazione, orientamento e decisioni documentate?
3. Come misurare correttezza delle risposte, qualità dei rinvii normativi e accessibilità cognitiva?
4. Come progettare con persone interessate, operatori e imprese accomodamenti e percorsi di inclusione?
5. Quali sono i limiti delle risposte automatizzate in materia di diritti soggettivi?

Le domande sopra sono **linee progettuali** e non risultati empirici dimostrati. Non trasferire qui dati individuali o indagini non autorizzate alla diffusione. Per il contesto generale v. [visione scientifica](docs/visione-scientifica.md).

## 2. Banca dati normativa: strutture e copertura (ricontrollo 16/11/2026; seed aggiornato al 08/11/2026)
**Stato dei file GitHub al 16/11/2026 (non certificazione normativa):**
- **63 atti censiti** in [`app/seed.json`](app/seed.json).
- **33 schede di articolo** relative a **2 atti pilota**: Legge 68/1999 e D.Lgs. 216/2003.
- **61 atti** sono catalogati **solo a livello di atto**.
- Il [catalogo documentale](normativa/CATALOGO-NORMATIVO-1994-2026.md) ha ricevuto integrazioni il **9 e il 16 novembre**, ma il **seed resta a 63 atti**, con ultimo aggiornamento interno 08/11/2026. Le nuove fonti **non sono ancora state implementate** nel database.
- **0 testi XML integrali ufficiali distribuiti nel repository** per l'intero corpus; **0 articoli con attestazione giuridica completa**.
- Archiviazione SQLite e importatori/analizzatori software presenti. La **presenza di codice** non prova l'esito dei test o un'importazione già eseguita.

**Documenti principali:**
- [Catalogo permanente 1994–2026](normativa/CATALOGO-NORMATIVO-1994-2026.md).
- [Integrazione multisito delle fonti](normativa/INTEGRAZIONE-MULTISITO-2026-11-08.md).
- [Indice preliminare delle fonti](normativa/indice-fonti.md).
- [Archivio atti e schede articolo](app/seed.json).
- [Descrizione dello stato tecnico e limiti](docs/STATO-IMPLEMENTAZIONE.md).

**Famiglie di norme trattate:** collocamento mirato, quote e convenzioni, accertamento della disabilità, obblighi dei datori, antidiscriminazione e accomodamenti, concorsi e DSA, congedi e assistenza, lavoro pubblico, reinserimento INAIL, cooperazione/impresa sociale, sicurezza, privacy dei dati sanitari, accessibilità digitale, IA e selezione, norme UE e prime fonti regionali.

**Aggiornamenti documentali da integrare nel seed:** il 09/11 sono state registrate tre integrazioni retrospettive (DM 23/07/2026 incentivi, DPR 12/03/2026 Piano, CGUE C-597/24). Il 16/11 il catalogo ha registrato il **D.Lgs. 208/2026**, pubblicato in GU il 14/11/2026 e con entrata in vigore indicata al **02/12/2026**: al 16/11 **non è ancora in vigore**. Riguarda il lavoro tramite piattaforme digitali e, secondo la ricognizione documentata nel catalogo § 15, l'art. 6 disciplina anche l'inferenza della disabilità dai dati nei sistemi automatizzati. Il riferimento alla direttiva (UE) 2024/2831 è presente nel catalogo, ma la sua versione consolidata non è stata riverificata direttamente su EUR-Lex. Queste schede non equivalgono a testi integrali importati o a una validazione giuridica articolo per articolo. Consultare il [catalogo, sezioni 14–15](normativa/CATALOGO-NORMATIVO-1994-2026.md) per fonti, date e limiti.

**Esempi fondamentali (non elenco esaustivo):** L. 104/1992; L. 68/1999; DPR 333/2000; direttiva 2000/78/CE; D.Lgs. 216/2003; L. 67/2006; L. 18/2009 e Convenzione ONU; L. 170/2010 (DSA, pertinenza differenziata); D.Lgs. 151/2015; D.Lgs. 62/2024; L. 106/2025; Regolamento UE 2024/1689. Usare per ciascuno la fonte e la specifica versione temporale, non questa sintesi.

## 3. Critic: verifica della conferenza e della vigenza
Esistono tre livelli distinti:
1. **Critic metadati** [`critic/critic.py`](critic/critic.py): campi, domini, possibili duplicati, rischi e classificazione preliminare.
2. **Critic documentale** [`app/legal_critic.py`](app/legal_critic.py): ricerca ed evidenze *solo in articoli importati*, senza promozione automatica a vigente.
3. **Audit di vigenza documentato** [`critic/AUDIT-VIGENZA-2026-11-08.md`](critic/AUDIT-VIGENZA-2026-11-08.md), [JSON](critic/audit-vigenza-2026-11-08.json), [lettore degli stati](critic/vigenza_status.py).

### Fotografia dell'audit (8/11/2026)
- **63 atti complessivi**.
- **45 fonti con una traccia istituzionale associata** (categorie eterogenee, non tutte attuali).
- **18 fonti senza verifica individuale nell'audit**.
- Classificazioni nell'audit: 30 atti con vigenza riscontrata a livello di atto, 2 con articolo consultabile, 1 con abrogazione parziale, 3 con solo testo originario, 1 con abrogazione da documentare puntualmente, 4 atti amministrativi pubblicati ma con operatività da controllare, 4 circolari rintracciate, 18 da verificare.
- **0 articoli/commi certificati da revisione completa**.
- Il file audit JSON **non è stato aggiornato** con la nuova fonte del 16/11; i suoi 63 record e le statistiche descrivono ancora il perimetro dell'08/11. Non includere la nuova fonte nelle percentuali di verifica senza aggiornare prima il dataset e rifare l'audit.

**Regola vincolante:** una legge può comparire come atto vigente pur contenendo articoli abrogati, modificati o con efficacia futura. Il Critic **non deve mai dedurre** vigenza da HTTP 200, URL valido, hash invariato, testo originario o semplice presenza di una scheda. Le circolari sono atti amministrativi da valutare per attualità operativa, non leggi. I regolamenti UE possono avere scadenze applicative differenziate.

### Classi di pertinenza
- **Diretta:** disciplina esplicita di diritti, obblighi o procedure connessi al lavoro.
- **Condizionata:** dipende da requisiti, territorio, settore, situazione o decorrenza.
- **Complementare:** sicurezza, privacy, accessibilità, formazione e contesto senza diritto lavorativo specifico deducibile da solo.
- **Contesto/Storica:** programmazione o testo non più applicabile come disciplina attuale.
- **Non pertinente:** giustificazione insufficiente per una risposta giuridica sul quesito.

Per i giudizi motivati è indispensabile associare **articolo + comma + testo/versione + data + fonte ufficiale + ragione + revisore**.

## 4. Software effettivamente pubblicato
| Percorso | Funzione | Limite |
|---|---|---|
| [`app/legislation.py`](app/legislation.py) | SQLite; inizializzazione, ricerca, consultazione e import articolo | Schede non equivalgono al testo ufficiale |
| [`app/official_ingest.py`](app/official_ingest.py) | Ingestion XML, hash, estrazione articolo, tracciamento | Parser euristico: controllare XML reali e date |
| [`app/fetch_official.py`](app/fetch_official.py) | Download da URL XML ufficiale puntuale con controlli host | Non è un crawler completo dei 63 atti |
| [`app/audit.py`](app/audit.py) | Report copertura testi/revisioni | Stato locale non sempre coincide con GitHub |
| [`app/legal_critic.py`](app/legal_critic.py) | Evidenze testuali e pertinenza lessicale | Non costituisce parere legale o certificazione |
| [`monitor/monitor.py`](monitor/monitor.py) | Fingerprint pagine istituzionali | Un cambiamento pagina non implica modifica di legge |
| [`.github/workflows/check-normativa.yml`](.github/workflows/check-normativa.yml) | Monitor tecnico settimanale e test | Esiti di esecuzione da verificare su GitHub Actions |
| [`tests/`](tests/) | Test unitari e sintetici | Non sostituiscono collaudi end-to-end su fonti reali |

**Ambiente:** Python 3.10+ con SQLite (standard library per i moduli essenziali). Non esiste ancora un'applicazione web completa pubblicata; non promettere URL di produzione. Progetto di accessibilità: obiettivo WCAG 2.2 AA.

## 5. Fonti istituzionali prioritarie
- [Normattiva](https://www.normattiva.it/) e [Normattiva Open Data](https://dati.normattiva.it/).
- [Gazzetta Ufficiale](https://www.gazzettaufficiale.it/).
- [Ministero del Lavoro](https://www.lavoro.gov.it/).
- [EUR-Lex](https://eur-lex.europa.eu/).
- [INPS](https://www.inps.it/) e [INAIL](https://www.inail.it/).
- [Funzione pubblica](https://www.funzionepubblica.gov.it/) per concorsi e pubblico impiego.
- [AgID](https://www.agid.gov.it/) per accessibilità.
- Portali ufficiali regionali e Bollettini ufficiali.

Conservare URL **puntuali** degli atti, non soltanto la homepage dell'ente. Quando una fonte è in PDF o formato complesso, preservare versione e tracciabilità senza inventare una trascrizione.

## 6. Decisioni progettuali finora adottate
1. **Un solo repository**, quello esistente `saracitano/normativadisabilitalavoro`, senza crearne altri.
2. **Un solo MASTERFILE canonico alla radice**, con link ai dettagli e cronologia delle revisioni via Git.
3. **Corpus 1994–oggi**, con inclusione di norme antecedenti rilevanti.
4. **Non solo elenco:** implementare testi normativi reali, versione e articolo/comma, collegamenti modificativi e ricerca.
5. **Critic obbligatorio:** distingue fonte autenticata, pertinenza, vigenza giuridica, applicazione individuale e qualità della risposta.
6. **Monitoraggio continuativo:** novità su fonti ufficiali, alert, revisione; mai presentare il monitor HTTP come certificazione.
7. **Accessibilità e inclusione:** linguaggio chiaro, alternative all'interfaccia complessa, partecipazione delle persone interessate.
8. **Protezione dati:** minimizzazione GDPR, dati sanitari non necessari da non acquisire; repository pubblico.
9. **Tracciamento del lavoro:** commit leggibili, verifiche riproducibili, attività aperte esplicite; niente dichiarazioni di lavoro completato senza prova.
10. **Separazione contenuto pubblico/riservato:** non pubblicare dataset, dati degli studenti/partecipanti, materiali interni o manoscritti non autorizzati.

## 7. Registro delle lacune e priorità operative
### Priorità alta
- **Riconciliare catalogo e database:** valutare l'inserimento nel seed del D.Lgs. 208/2026 e delle altre fonti documentate il 09/11, registrando date di pubblicazione/entrata in vigore e applicabilità; aggiornare solo allora il conteggio degli atti e l'audit.
- **Rivedere il monitor tecnico:** il [rapporto del 09/11](monitor/latest-report.json) registra **15 URL controllati** e **48 URL generici saltati** su 63 atti; migliorare i permalink prima di attribuire copertura al monitor. Baseline/hash non dimostrano vigenza.
- Completare **le 18 verifiche individuali ancora aperte** e rivedere le evidenze già presenti con URL e controllo della versione esatta.
- Acquisire via canali ufficiali i testi **integrali** delle 63 fonti rilevanti, distinguendo leggi da atti amministrativi e fonti storiche.
- Popolare articoli e commi; costruire **relazioni di modifica/abrogazione/efficacia differita**.
- Validare con prove le disposizioni più centrali: L. 68/1999, D.Lgs. 216/2003, DPR 333/2000, L.104/1992, D.Lgs.62/2024, norme DSA.
- Rendere l'audit del Critic riproducibile con per-articolo dati, fonte, checksum e motivazione; introdurre processo di revisione umana.
- Accertare effettivo funzionamento dei workflow e dei test nel repository.

### Priorità successiva
- Estendere fonti regionali a 20 Regioni e Province autonome; integrare attuativi, circolari vigenti e giurisprudenza pertinente.
- Implementare interfaccia web accessibile e ricerca normativa con RAG ancorata agli articoli verificati.
- Disegnare e sottoporre a revisione il protocollo di ricerca/valutazione con utenti e stakeholder, senza confondere ipotesi con risultati.
- Bibliografia scientifica referata: integrare solo dopo verifica di titolo, autori, anno, DOI e contenuti.

## 8. Protocolli di aggiornamento del masterfile
**Quando aggiornare:** ogni volta che un intervento modifica dati del catalogo, stato di vigenza, codice, audit, decisioni scientifiche, documentazione, roadmap o priorità. In aggiunta, eseguire una **riconciliazione periodica** degli ultimi commit del repository.

**Come:**
1. Leggere `MASTERFILE.md` e i file cambiati dall'ultimo commit.
2. Integrare informazioni nuove, correggere conteggi e riferimenti, preservare distinzioni fra *fatto, proposta, fonte e risultato*.
3. Aggiornare la data, la sezione delle priorità e il registro qui sotto.
4. Scrivere il masterfile con **commit separato e descrittivo**; mantenere la cronologia Git.
5. Verificare che i collegamenti funzionino, che i numeri derivino dai file reali e che nessuna informazione riservata sia stata pubblicata.
6. In caso di conflitto tra due revisioni, non sovrascrivere silenziosamente: confrontare le modifiche.

**Limite importante:** un nuovo messaggio in ChatGPT **non aggiorna automaticamente GitHub**. L'aggiornamento richiede una modifica esplicita tramite accesso GitHub o un'attività automatizzata autorizzata. Il monitor delle norme può aggiornare lo stato tecnico, **non** il contenuto delle nuove conversazioni non salvate.

### Registro revisioni del masterfile
| Data | Versione | Modifica |
|---|---|---|
| 2026-11-08 | 1.0 | Creato masterfile canonico, consolidamento di progetto, ricerca, codice, normativo, Critic, audit e protocollo di continuità |
| 2026-11-09 | 1.1 | Ricognizione ufficiale normativa: tre integrazioni retrospettive nel catalogo (DM 23/07/2026 incentivi, DPR 12/03/2026 Piano, CGUE C-597/24); nessuna nuova pubblicazione successiva all'8/11 confermata; vigenza articolo per articolo non certificata |
| 2026-11-16 | 1.2 | Nuovo D.Lgs. 208/2026 pubblicato il 14/11, con entrata in vigore indicata al 02/12/2026: protezione dati sulla disabilità nel lavoro mediante piattaforme digitali (art. 6), trasparenza e supervisione; scheda documentata nel catalogo § 15. Database seed ancora 63 atti: **non** aggiornato. Ricognizione UE e GU 13/11 non esaustiva |
| 2026-11-16 | 1.3 | Riconciliazione con README, seed, audit, catalogo e commit recenti; corretta intestazione ferma a 1.1, distinta la nuova fonte nel catalogo dai 63 atti del database; registrato monitor 09/11 (15 URL controllati, 48 generici esclusi); aggiunte priorità per integrazione e controllo temporale. Nessuna certificazione articolo/comma |

## 9. Come riprendere il lavoro in una nuova chat
**Testo da incollare nella nuova chat:**

> Stiamo lavorando al progetto Neurodivergenza Diversità al lavoro / NeuroLex Lavoro. Il repository canonico è https://github.com/saracitano/normativadisabilitalavoro . Leggi prima il file MASTERFILE.md e poi README.md, docs/STATO-IMPLEMENTAZIONE.md, app/seed.json e critic/audit-vigenza-2026-11-08.json. Verifica gli ultimi commit, identifica ciò che è implementato e ciò che resta aperto. Continua l'attività richiesta senza creare un secondo repository, e aggiorna il MASTERFILE quando modifichi il progetto. Non confondere schede, testi integrali, vigenza degli atti e vigenza delle disposizioni.

## 10. Copia sul PC Windows
Vedi [istruzioni di clonazione e sincronizzazione](docs/CLONARE-SU-WINDOWS.md). La copia locale è una *clone* Git; per scaricare aggiornamenti usare `git pull` quando non si hanno modifiche locali non salvate. Per inviare modifiche a GitHub servono accesso e permessi.
