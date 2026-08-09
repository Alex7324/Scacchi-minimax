"""Perft: il test standard per verificare la generazione delle mosse.

L'idea e' semplice: si contano TUTTE le posizioni raggiungibili in N mosse
a partire da una posizione data. Quei numeri sono noti e verificati, quindi
se il conteggio non combacia c'e' un bug nelle regole. E' molto piu' severo
di provare qualche mossa a mano: a profondita' 4 dalla posizione iniziale
si passa da 197281 posizioni, e ne basta una sbagliata per far saltare il totale.

Uso:
    python test_perft.py        prova fino a profondita' 3
    python test_perft.py 4      prova fino a profondita' 4 (piu' lento)
"""

import sys
import time

from scacchiera import copia_board, mosse_del_turno, esegui_mossa, nome_casella


def da_fen(fen):
    # il FEN e' il modo standard di scrivere una posizione in una riga.
    # usa le stesse convenzioni nostre: lettere per i pezzi, maiuscolo
    # per il bianco, e la prima riga e' l'ottava traversa
    parti = fen.split()

    board = []
    for riga in parti[0].split('/'):
        fila = []
        for ch in riga:
            if ch.isdigit():
                fila.extend('.' * int(ch))   # una cifra = tante caselle vuote
            else:
                fila.append(ch)
        board.append(fila)

    en_passant = None
    if parti[3] != '-':
        en_passant = (8 - int(parti[3][1]), 'abcdefgh'.index(parti[3][0]))

    return {
        'board': board,
        'tocca_al_bianco': parti[1] == 'w',
        'arrocco': {k: (k in parti[2]) for k in 'KQkq'},
        'en_passant': en_passant,
    }


def copia_partita(partita):
    return {
        'board': copia_board(partita['board']),
        'tocca_al_bianco': partita['tocca_al_bianco'],
        'arrocco': dict(partita['arrocco']),
        'en_passant': partita['en_passant'],
    }


def perft(partita, profondita):
    if profondita == 0:
        return 1

    totale = 0
    for partenza, arrivo in mosse_del_turno(partita):
        figlia = copia_partita(partita)
        esegui_mossa(figlia, partenza, arrivo)
        totale += perft(figlia, profondita - 1)

    return totale


def divide(partita, profondita):
    # perft spezzato per mossa iniziale. quando un totale non torna,
    # confrontare questi numeri con quelli di un motore che funziona
    # dice SUBITO da quale mossa nasce il problema
    risultati = {}

    for partenza, arrivo in mosse_del_turno(partita):
        figlia = copia_partita(partita)
        esegui_mossa(figlia, partenza, arrivo)
        chiave = nome_casella(partenza) + nome_casella(arrivo)
        risultati[chiave] = perft(figlia, profondita - 1)

    return risultati


# posizioni di riferimento: le prime due sono quelle che si usano
# ovunque per validare un motore. non sono scelte a caso, ognuna
# mette alla prova una parte diversa delle regole
POSIZIONI = [
    ('iniziale',
     'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -',
     [20, 400, 8902, 197281]),

    ('kiwipete: arrocchi da entrambi i lati, molte catture',
     'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -',
     [48, 2039, 97862]),

    ('finale con en passant e scacchi di scoperta',
     '8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - -',
     [14, 191, 2812, 43238]),

    ('promozioni, anche catturando',
     'r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq -',
     [6, 264, 9467]),

    ('pedone che promuove con il re sotto pressione',
     'rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ -',
     [44, 1486, 62379]),
]


def main():
    limite = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    falliti = 0

    for nome, fen, attesi in POSIZIONI:
        print('===', nome)

        for profondita, atteso in enumerate(attesi[:limite], start=1):
            partita = da_fen(fen)

            inizio = time.time()
            ottenuto = perft(partita, profondita)
            durata = time.time() - inizio

            if ottenuto == atteso:
                esito = 'OK'
            else:
                esito = 'ERRORE'
                falliti += 1

            print('  perft(%d)  atteso %-8d ottenuto %-8d  %-7s (%.1fs)'
                  % (profondita, atteso, ottenuto, esito, durata), flush=True)

    print()
    if falliti:
        print(falliti, 'conteggi sbagliati')
    else:
        print('tutti i conteggi corretti')


if __name__ == '__main__':
    main()
