# Motore di scacchi in Python

Scacchiera e motore di gioco scritti in Python puro, senza librerie esterne e
senza librerie di scacchi: le regole sono implementate da zero.

L'obiettivo finale è un motore che sceglie le proprie mosse con l'algoritmo
**minimax** e la **potatura alfa-beta**, con un'interfaccia web che permetta di
giocarci dal browser.

## Stato del progetto

In sviluppo. Attualmente implementati:

- rappresentazione della scacchiera e stampa da terminale
- generazione delle mosse di tutti i pezzi: pedone, torre, cavallo, alfiere,
  donna, re

Le mosse generate sono **pseudo-legali**: descrivono dove un pezzo può arrivare
in base al proprio movimento, ma non tengono conto dello scacco. Il re può
quindi raggiungere una casella attaccata, e un pezzo può muoversi anche quando
ciò espone il proprio re. Il rilevamento dello scacco non è ancora
implementato.

## Requisiti e avvio

Richiede Python 3. Nessuna dipendenza da installare.

```bash
python scacchiera.py
```

Vengono stampate la posizione iniziale e alcuni esempi di generazione delle
mosse.

## Rappresentazione della scacchiera

Una **lista di 8 liste**, una per riga, con accesso `board[riga][colonna]`.

I pezzi sono lettere singole, secondo la notazione FEN:

| lettera | pezzo   |
| ------- | ------- |
| `p`     | pedone  |
| `r`     | torre   |
| `n`     | cavallo |
| `b`     | alfiere |
| `q`     | donna   |
| `k`     | re      |

**Maiuscolo = bianco**, **minuscolo = nero**, `.` = casella vuota.

La riga `0` della lista corrisponde alla riga **8** della scacchiera, quella dei
pezzi neri; la riga `7` corrisponde alla riga **1**, quella dei pezzi bianchi.
In questo modo la scacchiera si stampa nell'ordine in cui è memorizzata, senza
inversioni, e il bianco avanza verso indici di riga decrescenti.

Le caselle sono tuple `(riga, colonna)`: la torre in a1 è `(7, 0)`. La funzione
`nome_casella` converte una tupla nella notazione scacchistica corrispondente.

## Struttura del codice

Negli scacchi i modi di muoversi sono sostanzialmente due, e il codice è
organizzato attorno a questa distinzione invece di ripetere la stessa logica per
ogni pezzo:

- `mosse_scorrevoli` — torre, alfiere e donna, che scorrono lungo una direzione
  finché non incontrano un bordo o un pezzo. Cambia solo l'elenco delle
  direzioni: la donna è l'unione di quelle della torre e dell'alfiere.
- `mosse_di_un_passo` — cavallo e re, che raggiungono una lista fissa di caselle
  senza scorrere.

Il pedone ha una funzione dedicata, essendo l'unico pezzo che si muove in un
modo e cattura in un altro.

`mosse(board, casella)` individua il pezzo presente sulla casella e delega alla
funzione corrispondente.

## Roadmap

Regole del gioco:

- [x] scacchiera, stampa e spostamento di un pezzo
- [x] mosse pseudo-legali di tutti i pezzi
- [ ] rilevamento dello scacco
- [ ] mosse legali: esclusione di quelle che lasciano il proprio re sotto scacco
- [ ] scacco matto e stallo
- [ ] arrocco, en passant, promozione del pedone

Motore:

- [ ] funzione di valutazione della posizione (materiale, poi posizione dei pezzi)
- [ ] ricerca con minimax
- [ ] potatura alfa-beta
- [ ] livelli di difficoltà, regolando la profondità di ricerca

Interfaccia:

- [ ] partita giocabile da terminale
- [ ] interfaccia web con scacchiera cliccabile

## Scelte di progetto

**Nessuna bitboard.** Sono la rappresentazione adottata dai motori più
performanti, ma complicano sensibilmente la parte più corposa del lavoro, cioè
la generazione delle mosse legali. Con una lista 8×8 il codice resta leggibile;
l'ottimizzazione della rappresentazione è eventualmente un passo successivo.

**Nessuna libreria di scacchi.** L'implementazione delle regole rientra tra gli
obiettivi del progetto e non viene delegata a dipendenze esterne.
