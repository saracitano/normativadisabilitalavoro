# Clonare il repository NeuroLex su un PC Windows

Questo documento fornisce i passaggi per creare **una copia locale reale** del repository GitHub. La clonazione avviene **sul tuo computer**, non sul sistema remoto di ChatGPT.

## Metodo 1 — PowerShell con Git (consigliato)

1. Apri PowerShell (Start → cerca PowerShell).
2. Controlla Git:
   ```powershell
   git --version
   ```
   Se il comando non è riconosciuto, installa **Git for Windows** da https://git-scm.com/downloads/win , quindi riapri PowerShell.
3. Esegui:
   ```powershell
   cd "$HOME\Documents"
   git clone https://github.com/saracitano/normativadisabilitalavoro.git
   cd normativadisabilitalavoro
   git status
   ```
   La cartella sarà `Documenti\normativadisabilitalavoro`. Se esiste già, **non clonare sopra**: aprila, verifica che sia una repository Git, e usa `git pull --ff-only`.

## Aggiornare la copia locale
```powershell
cd "$HOME\Documents\normativadisabilitalavoro"
git status
git pull --ff-only
```
Se `git status` mostra modifiche non salvate o `git pull` segnala divergenza, **non usare comandi distruttivi** come `reset --hard`: occorre prima decidere come conservare i cambiamenti.

## Modificare i documenti sul PC e pubblicarli
Per inviare modifiche a GitHub, se hai i permessi necessari e un metodo di autenticazione GitHub configurato:
```powershell
git add MASTERFILE.md
git commit -m "docs: aggiorna masterfile progetto"
git push origin main
```
Non inserire password o token direttamente nei comandi; usare un gestore credenziali sicuro.

## Metodo 2 — GitHub Desktop
Installa https://desktop.github.com/ , accedi con GitHub, scegli **File → Clone repository → URL**, incolla
`https://github.com/saracitano/normativadisabilitalavoro`, scegli la cartella locale e premi **Clone**. Poi usa **Fetch origin / Pull origin** per ricevere gli aggiornamenti.

## Aprire il masterfile
Dal browser:
https://github.com/saracitano/normativadisabilitalavoro/blob/main/MASTERFILE.md

Sul PC:
`Documenti\normativadisabilitalavoro\MASTERFILE.md`.

## Nota sulla privacy
Il repository attualmente è pubblico: non aggiungere qui dati sanitari, dati personali, materiali di ricerca riservati o manoscritti inediti.
