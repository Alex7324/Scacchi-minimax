# Motore di scacchi in Python

Progetto di studio: una scacchiera e un motore che valuta la posizione e gioca
contro un avversario umano, scritto in Python senza librerie esterne.

L'obiettivo finale è arrivare a un motore che sceglie le proprie mosse con
l'algoritmo **minimax** e la **potatura alfa-beta**, con un'interfaccia web per
poterci giocare comodamente dal browser.

## Stato attuale

Il progetto è in costruzione. Al momento funziona:

- rappresentazione della scacchiera e stampa da terminale
- generazione delle mosse di tutti i pezzi: pedone, torre, cavallo, alfiere,
  donna, re

Le mosse generate sono **pseudo-legali**: dicono dove un pezzo può arrivare
secondo il proprio movimento, ma non tengono ancora conto dello scacco. Il re
può quindi finire su una casella attaccata, e un pezzo può muoversi anche se
così espone il proprio re. È il prossimo pezzo di lavoro.

## Come provarlo

Serve solo Python 3, nessuna dipendenza da installare.

```bash
python scacchiera.py
```

Stampa la posizione iniziale e alcune prove di generazione delle mosse.

## Come è rappresentata la scacchiera

Una **lista di 8 liste**, una per riga, con accesso `board[riga][colonna]`.

I pezzi sono lettere singole, come nella notazione FEN:

| lettera | pezzo   |
| ------- | ------- |
| `p`     | pedone  |
| `r`     | torre   |
| `n`     | cavallo |
| `b`     | alfiere |
| `q`     | donna   |
| `k`     | re      |

**Maiuscolo = bianco**, **minuscolo = nero**, `.` = casella vuota.

La riga `0` della lista è la riga **8** della scacchiera (dove stanno i pezzi
neri) e la riga `7` è la riga **1** (pezzi bianchi). Quindi la scacchiera si
stampa così com'è, senza girarla, e il bianco "sale" verso righe di indice più
basso.

Le caselle si passano come tuple `(riga, colonna)`: la torre in a1 è `(7, 0)`.
La funzione `nome_casella` converte in notazione scacchistica per leggere
l'output a colpo d'occhio.

## Com'è organizzato il codice

Negli scacchi i modi di muoversi sono sostanzialmente due, e il codice segue
quella divisione invece di ripetere la stessa logica per ogni pezzo:

- `mosse_scorrevoli` — per torre, alfiere e donna, che scivolano lungo una
  direzione finché non incontrano un bordo o un pezzo. Cambia solo l'elenco
  delle direzioni, e la donna è semplicemente torre + alfiere.
- `mosse_di_un_passo` — per cavallo e re, che hanno una lista fissa di caselle
  raggiungibili senza scorrere.

Il pedone ha una funzione tutta sua, perché è l'unico pezzo che si muove in un
modo e mangia in un altro.

`mosse(board, casella)` guarda che pezzo c'è e chiama la funzione giusta.

## Obiettivi

Regole del gioco:

- [x] scacchiera, stampa e spostamento di un pezzo
- [x] mosse pseudo-legali di tutti i pezzi
- [ ] rilevamento dello scacco
- [ ] mosse legali: scartare quelle che lasciano il proprio re sotto scacco
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

**Niente bitboard.** Sono la rappresentazione usata dai motori seri e sarebbero
più veloci, ma rendono molto più difficile la parte più lunga del lavoro — la
generazione delle mosse legali. Con una lista 8×8 il codice resta leggibile e il
progetto arriva in fondo; l'ottimizzazione, semmai, viene dopo.

**Niente librerie di scacchi.** Le regole sono scritte a mano: il punto del
progetto è capirle, non delegarle.
