# Neurodivergenza Diversità al lavoro

Patrimonio scientifico, pedagogico, normativo e progettuale per promuovere l'accesso equo al mondo del lavoro delle persone neurodivergenti e con disabilità.

Questo repository ospita anche **NeuroLex Lavoro**, il progetto di applicazione web accessibile per ricercare e comprendere le norme italiane ed europee in tema di neurodivergenza, disabilità e lavoro, dal **1994 a oggi**, includendo disposizioni anteriori ancora rilevanti.

## Documentazione
- [Visione scientifica](docs/visione-scientifica.md)
- [Specifiche NeuroLex Lavoro](docs/neurolex-lavoro.md)
- [Indice preliminare delle fonti normative](normativa/indice-fonti.md)
- [Roadmap](docs/roadmap.md)
- [Governance delle conoscenze](docs/governance-conoscenza.md)

## Principi
Accessibilità, autodeterminazione, inclusione lavorativa, fonti verificabili, diritti, co-progettazione e tutela dei dati. Neurodivergenza e riconoscimento giuridico della disabilità non sono sinonimi: l'applicabilità delle misure dipende dai relativi requisiti.

## Stato
Documentazione progettuale iniziale — 8 novembre 2026. Le norme elencate richiedono verifica aggiornata su fonti ufficiali; l'applicazione non è ancora operativa.

## Riservatezza
Questo repository è **pubblico**. Non pubblicare informazioni sanitarie, dati personali, dataset non anonimizzati, bozze scientifiche inedite o documenti riservati senza le necessarie autorizzazioni. Le future integrazioni richiedono accesso GitHub e un'operazione di aggiornamento esplicita.

## Controllo critico delle fonti
- [Critic delle fonti: metodo e audit iniziale](critic/README.md)
- [Archivio strutturato delle schede](critic/fonti.csv)
- [Script di controllo riproducibile](critic/critic.py)

Il critic distingue pertinenza diretta, condizionata, complementare e contesto; la valutazione automatica dei metadati **non equivale** alla validazione giuridica dell'atto.

## Implementazione normativa sperimentale
- [Archivio articoli, ricerca SQLite e importazione versioni testuali](app/README.md)
- [Schede normative per articolo](app/seed.json)
- [Codice Python dell'archivio](app/legislation.py)

La prima release indicizza **33 schede di articoli** per L. 68/1999 e D.Lgs. 216/2003. Le sintesi non sostituiscono il testo integrale: il caricamento delle versioni ufficiali avviene mediante importazione tracciata e richiede revisione.

## Archivio ampliato e controllo delle fonti — novembre 2026
- [63 atti indicizzati con copertura documentata](app/seed.json) — 33 schede per articolo, altre fonti a livello di atto, da completare.
- [Ricerca nel database SQLite](app/README.md)
- [Monitoraggio tecnico delle fonti ufficiali](monitor/README.md)
- [GitHub Actions: controllo settimanale](.github/workflows/check-normativa.yml)

**Il monitor non certifica la vigenza**: identifica possibili modifiche tecniche delle pagine, indisponibilità e collegamenti generici. La validazione dell'efficacia normativa richiede controllo umano sul testo e sul regime temporale.
