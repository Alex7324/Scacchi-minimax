def board_iniziale():
    # restituisce una scacchiera NUOVA nella posizione di partenza.
    # e' una funzione e non una variabile globale cosi' ogni prova
    # parte da una scacchiera pulita, senza portarsi dietro le
    # modifiche fatte dalle prove precedenti
    return [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],   # riga 8 - pezzi neri
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],   # riga 7 - pedoni neri
        ['.', '.', '.', '.', '.', '.', '.', '.'],   # riga 6
        ['.', '.', '.', '.', '.', '.', '.', '.'],   # riga 5
        ['.', '.', '.', '.', '.', '.', '.', '.'],   # riga 4
        ['.', '.', '.', '.', '.', '.', '.', '.'],   # riga 3
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],   # riga 2 - pedoni bianchi
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],   # riga 1 - pezzi bianchi
    ]


def board_vuota():
    # scacchiera vuota, comoda per provare un pezzo singolo.
    # NON scrivere [['.'] * 8] * 8: creerebbe 8 riferimenti alla
    # STESSA riga, e cambiando una casella cambierebbero tutte
    return [['.' for _ in range(8)] for _ in range(8)]


def stampa(board):
    for riga in board:
        for pezzo in riga:
            print(pezzo, end=' ')
        print()


def muovi(board, partenza, arrivo):
    r1, c1 = partenza
    r2, c2 = arrivo
    board[r2][c2] = board[r1][c1]
    board[r1][c1] = '.'


def nome_casella(casella):
    # da (riga, colonna) a notazione scacchistica: (7, 0) -> "a1"
    r, c = casella
    return 'abcdefgh'[c] + str(8 - r)


# ---------------------------------------------------------------
# le direzioni, scritte una volta sola e riusate dai vari pezzi
# ---------------------------------------------------------------

DIREZIONI_TORRE = [(-1, 0), (1, 0), (0, -1), (0, 1)]            # croce
DIREZIONI_ALFIERE = [(-1, -1), (-1, 1), (1, -1), (1, 1)]        # diagonali
DIREZIONI_DONNA = DIREZIONI_TORRE + DIREZIONI_ALFIERE           # tutte e 8

SALTI_CAVALLO = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                 (1, -2), (1, 2), (2, -1), (2, 1)]


# ---------------------------------------------------------------
# i due modi di muoversi degli scacchi
# ---------------------------------------------------------------

def mosse_scorrevoli(board, casella, direzioni):
    # per torre, alfiere e donna: scivolano lungo una direzione
    # finche' qualcosa non le ferma.
    # e' esattamente il codice della torre di prima, con le direzioni
    # passate da fuori invece che scritte dentro
    r, c = casella
    io_sono_bianco = board[r][c].isupper()
    mosse = []

    for dr, dc in direzioni:
        nr = r + dr
        nc = c + dc

        while 0 <= nr < 8 and 0 <= nc < 8:
            contenuto = board[nr][nc]

            if contenuto == '.':
                # libera: ci vado e proseguo oltre
                mosse.append((nr, nc))
            else:
                # un pezzo mi sbarra la strada: questa direzione
                # finisce qui. se e' avversario lo posso mangiare,
                # quindi quella casella vale come mossa
                if contenuto.isupper() != io_sono_bianco:
                    mosse.append((nr, nc))
                break

            nr += dr
            nc += dc

    return mosse


def mosse_di_un_passo(board, casella, salti):
    # per cavallo e re: una lista fissa di caselle raggiungibili,
    # senza scorrere. niente while, solo un controllo per casella.
    # al cavallo non importa cosa c'e' in mezzo, perche' salta
    r, c = casella
    io_sono_bianco = board[r][c].isupper()
    mosse = []

    for dr, dc in salti:
        nr = r + dr
        nc = c + dc

        if 0 <= nr < 8 and 0 <= nc < 8:
            contenuto = board[nr][nc]
            # va bene se e' vuota, oppure se c'e' un avversario.
            # l'unica casella vietata e' quella con un pezzo mio
            if contenuto == '.' or contenuto.isupper() != io_sono_bianco:
                mosse.append((nr, nc))

    return mosse


# ---------------------------------------------------------------
# i pezzi
# ---------------------------------------------------------------

def mosse_torre(board, casella):
    return mosse_scorrevoli(board, casella, DIREZIONI_TORRE)


def mosse_alfiere(board, casella):
    return mosse_scorrevoli(board, casella, DIREZIONI_ALFIERE)


def mosse_donna(board, casella):
    # la donna e' letteralmente torre + alfiere insieme
    return mosse_scorrevoli(board, casella, DIREZIONI_DONNA)


def mosse_cavallo(board, casella):
    return mosse_di_un_passo(board, casella, SALTI_CAVALLO)


def mosse_re(board, casella):
    # stesse 8 direzioni della donna, ma un passo solo
    return mosse_di_un_passo(board, casella, DIREZIONI_DONNA)


def mosse_pedone(board, casella):
    r, c = casella
    io_sono_bianco = board[r][c].isupper()

    # il pedone e' l'unico pezzo che va in una sola direzione:
    # il bianco sale verso la riga 0, il nero scende verso la riga 7.
    # la riga iniziale mi serve per sapere se ha ancora il doppio passo
    if io_sono_bianco:
        avanti = -1
        riga_iniziale = 6
    else:
        avanti = 1
        riga_iniziale = 1

    mosse = []

    # 1) un passo avanti, ma solo se la casella davanti e' LIBERA.
    #    il pedone andando dritto non mangia mai
    nr = r + avanti
    if 0 <= nr < 8 and board[nr][c] == '.':
        mosse.append((nr, c))

        # 2) il doppio passo, solo dalla riga di partenza.
        #    e' annidato dentro l'if di sopra apposta: se la prima
        #    casella e' occupata il pedone non puo' scavalcarla,
        #    quindi la doppia non esiste nemmeno
        if r == riga_iniziale and board[r + 2 * avanti][c] == '.':
            mosse.append((r + 2 * avanti, c))

    # 3) le catture, solo in diagonale e solo se li' c'e' davvero
    #    un pezzo avversario. e' il contrario del movimento normale:
    #    in diagonale il pedone va SOLO se c'e' qualcosa da mangiare
    for dc in (-1, 1):
        nc = c + dc
        if 0 <= nr < 8 and 0 <= nc < 8:
            contenuto = board[nr][nc]
            if contenuto != '.' and contenuto.isupper() != io_sono_bianco:
                mosse.append((nr, nc))

    return mosse


def mosse(board, casella):
    # guarda che pezzo c'e' sulla casella e chiama la funzione giusta.
    # .lower() serve a trattare 'R' e 'r' allo stesso modo: le regole
    # di movimento sono le stesse, cambia solo il colore
    r, c = casella
    pezzo = board[r][c].lower()

    if pezzo == 'p':
        return mosse_pedone(board, casella)
    if pezzo == 'r':
        return mosse_torre(board, casella)
    if pezzo == 'n':
        return mosse_cavallo(board, casella)
    if pezzo == 'b':
        return mosse_alfiere(board, casella)
    if pezzo == 'q':
        return mosse_donna(board, casella)
    if pezzo == 'k':
        return mosse_re(board, casella)

    return []   # casella vuota: nessuna mossa


# ---------------------------------------------------------------
# prove
# ---------------------------------------------------------------

def prova(titolo, board, casella):
    trovate = [nome_casella(m) for m in mosse(board, casella)]
    print(titolo)
    print('  da', nome_casella(casella), '->', sorted(trovate))


b = board_iniziale()
stampa(b)
print()

prova('cavallo b1 (salta i suoi pedoni):', b, (7, 1))
prova('donna d1 (chiusa dai suoi pezzi):', b, (7, 3))
prova('pedone e2:', b, (6, 4))

print()

# scacchiera vuota con qualche pezzo piazzato a mano
b = board_vuota()
b[4][3] = 'Q'   # donna bianca in d4
b[4][6] = 'p'   # pedone nero in g4
b[6][3] = 'P'   # pedone bianco in d2
prova('donna d4, pedone nero in g4 e pedone bianco in d2:', b, (4, 3))

b = board_vuota()
b[0][0] = 'N'   # cavallo bianco in a8, nell'angolo
prova("cavallo in a8 (nell'angolo, meta' dei salti finisce fuori):", b, (0, 0))

b = board_vuota()
b[4][4] = 'K'   # re bianco in e4
b[3][4] = 'p'   # pedone nero in e5
b[5][4] = 'P'   # pedone bianco in e3
prova('re e4, pedone nero in e5 e pedone bianco in e3:', b, (4, 4))
