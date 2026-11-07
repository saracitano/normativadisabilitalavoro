# Critic delle fonti normative — protocollo scientifico e giuridico

**Modulo:** Critic NeuroLex Lavoro — versione 0.1 (8 novembre 2026).

## Scopo
Sottoporre ogni fonte del repertorio a una valutazione critica della **conferenza** con le domande del progetto: disabilità, neurodivergenza, accesso e mantenimento del lavoro, tutele, obblighi e percorsi occupazionali.

Il *critic* evita che ogni fonte che menziona una disabilità venga trattata come una norma che attribuisce direttamente un diritto lavorativo.

## Cinque passaggi di validazione
1. **Autenticità documentale:** ente emanante, testo ufficiale, identificativo, collegamento all'atto; il dominio istituzionale è solo un indizio, non una prova del contenuto.
2. **Pertinenza tematica:** l'atto disciplina concretamente lavoro o discriminazione nel lavoro? Oppure è solo contesto educativo, programmatico, sanitario o tecnologico?
3. **Applicabilità giuridica:** destinatari, definizioni, certificazioni richieste, soglie, territorio, settore pubblico/privato, tipo di rapporto, fase di inserimento.
4. **Vigenza e gerarchia:** testo storico, modifiche, abrogazioni, entrata in vigore e disciplina transitoria; distinguere regolamento, legge, circolare, interpretazione e strategia.
5. **Traduzione informativa:** quali domande dell'utente può legittimamente supportare? Quali affermazioni non sono sostenute? Articolo esatto, citazione, data, grado di incertezza e validazione umana.

## Esito della conferenza
- **Diretta:** fonte che regola esplicitamente diritti, obblighi o procedure relativi al lavoro delle persone con disabilità/neurodivergenza.
- **Condizionata:** norma rilevante solo per specifiche condizioni (territorio, requisiti di invalidità, settore, patologia, scadenza).
- **Complementare:** testo importante per cornice, privacy, accessibilità, sicurezza, formazione, ma non fonda di per sé una specifica tutela lavorativa per tutti.
- **Contesto:** documento programmatico o richiamo generale, utile per ricerca e interpretazione, non per attribuire un diritto immediato.
- **Non pertinente:** non giustifica l'inclusione nell'archivio del lavoro; spostare in bibliografia di contesto o escludere.

Queste classi **non costituiscono una graduatoria del valore giuridico delle fonti**.

## Criteri di esclusione o sospensione
- Dati bibliografici non rintracciabili o fonte non ufficiale senza verifica indipendente.
- Nessun collegamento spiegabile al lavoro e alla disabilità.
- Regime transitorio ignoto in quesiti che richiedono l'attuale applicabilità.
- Obbligo erroneamente dedotto da linee guida o strategie.
- Generalizzazioni quali «qualsiasi persona con ADHD ha diritto al collocamento mirato».
- Fonti regionali proposte come valide sull'intero territorio nazionale.
- Testo originario presentato come attualmente vigente.

## Come funziona il primo prototipo
Il file [fonti.csv](fonti.csv) contiene 20 schede iniziali con **classificazione proposta dall'editor**.
Lo script [critic.py](critic.py) controlla *offline* campi obbligatori, duplicati, dominio URL, classificazioni e segnali di rischio.
Esecuzione dalla radice del repository:

```bash
python3 critic/critic.py critic/fonti.csv > critic/audit.json
```

Il programma **non naviga il web, non legge gli articoli e non accerta la vigenza**. Le etichette in CSV non vanno scambiate per un giudizio indipendente prodotto dal software. Per un *critic* semantico completo serviranno acquisizione di testi ufficiali, retrieval per articolo, valutazione con prove, registro editoriale e revisione giuridica.

## Audit critico iniziale delle fonti principali

| Atto | Conferenza proposta | Limite determinante |
|---|---|---|
| Legge 68/1999 | **Diretta** | Presupposti di accesso al collocamento mirato non universali; testo e modifiche da controllare articolo per articolo |
| Direttiva 2000/78/CE e D.Lgs. 216/2003 | **Diretta** | Non discriminazione e accomodamento; analizzare presupposti, interpretazione e applicabilità |
| DM 43/2022 | **Diretta (attuativa)** | Linee guida per collocamento mirato, da non confondere con una nuova legge che crea automaticamente diritti individuali |
| Legge 170/2010 | **Complementare** | Essenzialmente DSA e istruzione: non basta da sola per dedurre automaticamente accomodamenti in qualunque azienda |
| D.L. 80/2021 e D.L. 4/2022 | **Diretta** | Distinguere concorsi pubblici e selezione lavorativa privata, e verificare i singoli commi |
| Legge 106/2025 | **Condizionata** | Congedi e conservazione del posto per casi definiti; soglia di invalidità e diagnosi rilevanti |
| D.Lgs. 62/2024 | **Diretta** | Accomodamento e valutazione; disposizioni transitorie e territori coinvolti |
| Regolamento UE 2024/1689 | **Condizionata** | Sistemi IA e HR; non tutte le disposizioni hanno la stessa data di applicazione |
| L.R. Lombardia 13/2003 | **Condizionata** | Valida nell'ambito territoriale e istituzionale competente |
| DPR secondo programma biennale 2017 | **Contesto** | Indirizzo programmatico, non fonte autonoma di obblighi immediatamente azionabili |
| Regolamento UE 2016/679 | **Complementare** | Privacy e dati particolari, essenziale al trattamento dati ma non tutela occupazionale speciale in sé |

## Esempio di valutazione di una risposta
**Domanda:** «Sono autistico: posso accedere al collocamento mirato?»
- Fonte appropriata: L. 68/1999 e disposizioni sull'accertamento pertinente.
- Verifica critica: la sola diagnosi non è equivalente al possesso dei requisiti legali di iscrizione.
- Fonte da evitare come prova sufficiente: legge sull'accessibilità digitale o strategia generale.
- Esito: risposta **condizionata ai requisiti**, senza conclusione automatica sull'utente.

## Riferimenti istituzionali controllati per l'impostazione
- [L. 68/1999 — Normattiva](https://www.normattiva.it/atto/caricaDettaglioAtto?atto.codiceRedazionale=099G0123&atto.dataPubblicazioneGazzetta=1999-03-23)
- [D.Lgs. 216/2003 — Normattiva](https://www.normattiva.it/atto/caricaDettaglioAtto?atto.codiceRedazionale=003G0240&atto.dataPubblicazioneGazzetta=2003-08-13)
- [DM 43/2022 — Ministero del Lavoro](https://www.lavoro.gov.it/documenti-e-norme/normative/pagine/decreto-ministeriale-n.-43-dell11-marzo-2022)
- [L. 106/2025 — Normattiva](https://www.normattiva.it/atto/caricaDettaglioAtto?atto.codiceRedazionale=25G00114&atto.dataPubblicazioneGazzetta=2025-07-25)

## Prossima fase progettuale
Sostituire i link generici con permalinks all'atto; aggiungere articoli e versioni, riesame umano motivato, controlli di aggiornamento e un audit semantico RAG con evidenze testuali. Ogni output del *critic* dovrà conservare la prova citata e il livello di revisione.
