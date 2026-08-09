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


def nome_casella(casella):
    # da (riga, colonna) a notazione scacchistica: (7, 0) -> "a1".
    # una mossa di promozione ha un terzo elemento con il pezzo
    # scelto, e in quel caso lo aggiungo in fondo: (0, 2, 'N') -> "c8=N"
    r = casella[0]
    c = casella[1]
    nome = 'abcdefgh'[c] + str(8 - r)

    if len(casella) == 3:
        nome += '=' + casella[2].upper()

    return nome


def copia_board(board):
    # copia VERA della scacchiera: una lista nuova per ogni riga.
    # attenzione, board[:] oppure list(board) NON bastano: creerebbero
    # una lista nuova che pero' contiene le STESSE otto righe, e
    # modificando la copia si modificherebbe anche l'originale
    return [riga[:] for riga in board]


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
    # finche' qualcosa non le ferma
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
    # senza scorrere. niente while, solo un controllo per casella
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


def mosse_pedone(board, casella, en_passant=None):
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

    arrivi = []

    # 1) un passo avanti, ma solo se la casella davanti e' LIBERA.
    #    il pedone andando dritto non mangia mai
    nr = r + avanti
    if 0 <= nr < 8 and board[nr][c] == '.':
        arrivi.append((nr, c))

        # 2) il doppio passo, solo dalla riga di partenza.
        #    e' annidato dentro l'if di sopra apposta: se la prima
        #    casella e' occupata il pedone non puo' scavalcarla,
        #    quindi la doppia non esiste nemmeno
        if r == riga_iniziale and board[r + 2 * avanti][c] == '.':
            arrivi.append((r + 2 * avanti, c))

    # 3) le catture, solo in diagonale e solo se li' c'e' davvero
    #    un pezzo avversario
    for dc in (-1, 1):
        nc = c + dc
        if 0 <= nr < 8 and 0 <= nc < 8:
            contenuto = board[nr][nc]
            if contenuto != '.' and contenuto.isupper() != io_sono_bianco:
                arrivi.append((nr, nc))

    # 4) EN PASSANT: l'unico caso in cui il pedone va in diagonale
    #    su una casella VUOTA. succede solo subito dopo che un pedone
    #    avversario ha fatto il doppio passo passandoci accanto
    if en_passant is not None:
        for dc in (-1, 1):
            if (nr, c + dc) == en_passant:
                arrivi.append(en_passant)

    # 5) PROMOZIONE: arrivare in fondo non e' UNA mossa ma QUATTRO.
    #    scegliere donna, torre, alfiere o cavallo porta a posizioni
    #    diverse, quindi il pezzo scelto fa parte della mossa e viaggia
    #    con lei come terzo elemento della tupla
    ultima_traversa = 0 if io_sono_bianco else 7
    scelte = 'QRBN' if io_sono_bianco else 'qrbn'

    mosse = []
    for arrivo in arrivi:
        if arrivo[0] == ultima_traversa:
            for pezzo_scelto in scelte:
                mosse.append((arrivo[0], arrivo[1], pezzo_scelto))
        else:
            mosse.append(arrivo)

    return mosse


def mosse_re(board, casella, arrocco=None):
    # stesse 8 direzioni della donna, ma un passo solo
    normali = mosse_di_un_passo(board, casella, DIREZIONI_DONNA)

    if arrocco is None:
        return normali

    return normali + mosse_arrocco(board, casella, arrocco)


def mosse_arrocco(board, casella, arrocco):
    # l'arrocco ha quattro condizioni, e servono tutte:
    #  - re e torre non si sono ancora mossi (lo dice il dizionario)
    #  - le caselle tra i due sono libere
    #  - il re non e' sotto scacco adesso
    #  - il re non attraversa una casella attaccata
    # la casella di ARRIVO non la controllo qui: ci pensa gia'
    # mosse_legali, che scarta le mosse che finiscono sotto scacco
    r, c = casella
    bianco = board[r][c].isupper()
    riga = 7 if bianco else 0

    # se il re non e' a casa sua non c'e' niente da fare
    if (r, c) != (riga, 4):
        return []

    if sotto_scacco(board, bianco):
        return []

    mosse = []
    lato_re = 'K' if bianco else 'k'
    lato_donna = 'Q' if bianco else 'q'

    # lato re: f e g libere, il re passa da f
    if arrocco.get(lato_re):
        if board[riga][5] == '.' and board[riga][6] == '.':
            if not casella_attaccata(board, (riga, 5), bianco):
                mosse.append((riga, 6))

    # lato donna: b, c e d libere, il re passa da d
    # (la casella b la attraversa la TORRE, e alla torre non importa
    #  se e' attaccata: solo il re non puo' passare sotto tiro)
    if arrocco.get(lato_donna):
        if board[riga][1] == '.' and board[riga][2] == '.' \
                and board[riga][3] == '.':
            if not casella_attaccata(board, (riga, 3), bianco):
                mosse.append((riga, 2))

    return mosse


def mosse(board, casella, en_passant=None, arrocco=None):
    # guarda che pezzo c'e' sulla casella e chiama la funzione giusta.
    # .lower() serve a trattare 'R' e 'r' allo stesso modo: le regole
    # di movimento sono le stesse, cambia solo il colore
    r, c = casella
    pezzo = board[r][c].lower()

    if pezzo == 'p':
        return mosse_pedone(board, casella, en_passant)
    if pezzo == 'r':
        return mosse_torre(board, casella)
    if pezzo == 'n':
        return mosse_cavallo(board, casella)
    if pezzo == 'b':
        return mosse_alfiere(board, casella)
    if pezzo == 'q':
        return mosse_donna(board, casella)
    if pezzo == 'k':
        return mosse_re(board, casella, arrocco)

    return []   # casella vuota: nessuna mossa


# ---------------------------------------------------------------
# eseguire una mossa sulla scacchiera
# ---------------------------------------------------------------

def applica(board, partenza, arrivo, en_passant=None):
    # sposta il pezzo gestendo i tre casi in cui una mossa cambia
    # la scacchiera in modo diverso dal solito "da qui a li'"
    r1, c1 = partenza
    r2 = arrivo[0]
    c2 = arrivo[1]
    # terzo elemento presente solo nelle mosse di promozione
    promozione = arrivo[2] if len(arrivo) == 3 else None
    pezzo = board[r1][c1]

    # EN PASSANT: il pedone catturato non sta sulla casella di arrivo,
    # sta di FIANCO al pedone che muove. va tolto a mano
    if pezzo.lower() == 'p' and (r2, c2) == en_passant:
        board[r1][c2] = '.'

    # ARROCCO: il re si sposta di due colonne e la torre lo scavalca.
    # e' l'unica mossa in cui si muovono due pezzi insieme
    if pezzo.lower() == 'k' and abs(c2 - c1) == 2:
        if c2 == 6:                     # lato re: la torre da h va in f
            board[r1][5] = board[r1][7]
            board[r1][7] = '.'
        else:                           # lato donna: la torre da a va in d
            board[r1][3] = board[r1][0]
            board[r1][0] = '.'

    board[r2][c2] = pezzo
    board[r1][c1] = '.'

    # PROMOZIONE: il pedone che arriva in fondo diventa il pezzo che
    # la mossa si porta dietro. se la mossa non lo dice (per esempio
    # quando si sposta un pezzo a mano in una prova) metto donna,
    # perche' un pedone sull'ultima traversa non e' una posizione valida
    if pezzo.lower() == 'p' and r2 in (0, 7):
        if promozione is not None:
            board[r2][c2] = promozione
        else:
            board[r2][c2] = 'Q' if pezzo.isupper() else 'q'


def muovi(board, partenza, arrivo):
    # spostamento semplice, senza stato di partita
    applica(board, partenza, arrivo)


# ---------------------------------------------------------------
# lo scacco
# ---------------------------------------------------------------

def caselle_attaccate(board, casella):
    # le caselle che un pezzo tiene SOTTO TIRO.
    # per quasi tutti i pezzi coincidono con le mosse, ma il pedone
    # fa eccezione: si muove in avanti e attacca in diagonale, e le
    # due cose non vanno confuse quando si guarda chi controlla cosa
    r, c = casella
    pezzo = board[r][c]

    if pezzo.lower() == 'p':
        avanti = -1 if pezzo.isupper() else 1
        attaccate = []
        for dc in (-1, 1):
            nr, nc = r + avanti, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                attaccate.append((nr, nc))
        return attaccate

    # niente arrocco qui: l'arrocco non cattura mai, e passare i
    # diritti farebbe chiamare sotto_scacco dentro sotto_scacco
    return mosse(board, casella)


def casella_attaccata(board, casella, bianco):
    # la casella e' sotto tiro di almeno un pezzo avversario?
    # "bianco" e' il colore di CHI SI DIFENDE
    for r in range(8):
        for c in range(8):
            pezzo = board[r][c]

            if pezzo == '.':
                continue
            if pezzo.isupper() == bianco:
                continue    # e' un pezzo mio: non mi attacca

            if casella in caselle_attaccate(board, (r, c)):
                return True

    return False


def trova_re(board, bianco):
    # scorre la scacchiera finche' non trova il re del colore chiesto
    re = 'K' if bianco else 'k'

    for r in range(8):
        for c in range(8):
            if board[r][c] == re:
                return (r, c)

    return None   # nessun re sulla scacchiera (capita solo nelle prove)


def sotto_scacco(board, bianco):
    # essere sotto scacco vuol dire esattamente una cosa:
    # la casella dove sta il mio re e' attaccata
    casella_re = trova_re(board, bianco)

    if casella_re is None:
        return False

    return casella_attaccata(board, casella_re, bianco)


# ---------------------------------------------------------------
# le mosse legali
# ---------------------------------------------------------------

def mosse_legali(board, casella, en_passant=None, arrocco=None):
    # una mossa e' legale se, DOPO averla fatta, il mio re non e'
    # sotto scacco. l'unico modo per saperlo e' provarla: la eseguo
    # su una copia della scacchiera e guardo com'e' finita
    r, c = casella
    pezzo = board[r][c]

    if pezzo == '.':
        return []

    io_sono_bianco = pezzo.isupper()
    legali = []

    for arrivo in mosse(board, casella, en_passant, arrocco):
        prova = copia_board(board)
        applica(prova, casella, arrivo, en_passant)

        # la scacchiera vera non e' stata toccata: ho mosso solo la copia
        if not sotto_scacco(prova, io_sono_bianco):
            legali.append(arrivo)

    return legali


def tutte_le_mosse_legali(board, bianco, en_passant=None, arrocco=None):
    # tutte le mosse che un colore puo' fare, come coppie
    # (partenza, arrivo). e' la lista da cui il motore scegliera'
    tutte = []

    for r in range(8):
        for c in range(8):
            pezzo = board[r][c]

            if pezzo == '.' or pezzo.isupper() != bianco:
                continue

            for arrivo in mosse_legali(board, (r, c), en_passant, arrocco):
                tutte.append(((r, c), arrivo))

    return tutte


# ---------------------------------------------------------------
# fine partita
# ---------------------------------------------------------------

def scacco_matto(board, bianco, en_passant=None, arrocco=None):
    # nessuna mossa disponibile E il re sotto attacco: hai perso
    return (sotto_scacco(board, bianco)
            and not tutte_le_mosse_legali(board, bianco, en_passant, arrocco))


def stallo(board, bianco, en_passant=None, arrocco=None):
    # nessuna mossa disponibile ma il re NON e' sotto attacco:
    # la partita finisce patta. e' l'unico caso in cui non poter
    # muovere non e' una sconfitta
    return (not sotto_scacco(board, bianco)
            and not tutte_le_mosse_legali(board, bianco, en_passant, arrocco))


# ---------------------------------------------------------------
# la partita: la scacchiera piu' quello che la scacchiera non dice
# ---------------------------------------------------------------

def partita_iniziale():
    # arrocco ed en passant non si possono dedurre guardando la
    # scacchiera: dipendono da cosa e' successo PRIMA. quindi oltre
    # alla posizione serve tenersi da parte un po' di storia
    return {
        'board': board_iniziale(),
        'tocca_al_bianco': True,
        # K = bianco lato re, Q = bianco lato donna, minuscole = nero
        'arrocco': {'K': True, 'Q': True, 'k': True, 'q': True},
        'en_passant': None,
    }


def mosse_del_pezzo(partita, casella):
    return mosse_legali(partita['board'], casella,
                        partita['en_passant'], partita['arrocco'])


def mosse_del_turno(partita):
    return tutte_le_mosse_legali(partita['board'], partita['tocca_al_bianco'],
                                 partita['en_passant'], partita['arrocco'])


def esegui_mossa(partita, partenza, arrivo):
    board = partita['board']
    r1, c1 = partenza
    r2 = arrivo[0]
    c2 = arrivo[1]
    pezzo = board[r1][c1]

    applica(board, partenza, arrivo, partita['en_passant'])

    # l'en passant vale SOLO per la mossa immediatamente successiva:
    # o lo sfrutti subito o il diritto scade
    if pezzo.lower() == 'p' and abs(r2 - r1) == 2:
        partita['en_passant'] = ((r1 + r2) // 2, c1)
    else:
        partita['en_passant'] = None

    # i diritti di arrocco invece si perdono PER SEMPRE, appena il re
    # o una torre si muovono. e anche se la torre viene mangiata:
    # per questo guardo sia la partenza sia l'arrivo
    diritti = partita['arrocco']

    if pezzo == 'K':
        diritti['K'] = False
        diritti['Q'] = False
    elif pezzo == 'k':
        diritti['k'] = False
        diritti['q'] = False

    # uso (r2, c2) e non "arrivo": una mossa di promozione ha tre
    # elementi e non combacerebbe mai con un angolo. serve davvero,
    # perche' un pedone puo' promuovere CATTURANDO la torre nell'angolo
    for angolo in (partenza, (r2, c2)):
        if angolo == (7, 7):
            diritti['K'] = False
        elif angolo == (7, 0):
            diritti['Q'] = False
        elif angolo == (0, 7):
            diritti['k'] = False
        elif angolo == (0, 0):
            diritti['q'] = False

    partita['tocca_al_bianco'] = not partita['tocca_al_bianco']


# ---------------------------------------------------------------
# prove
# ---------------------------------------------------------------

def elenco(mosse_trovate):
    return sorted(nome_casella(m) for m in mosse_trovate)


def prove():
    print('--- matto e stallo ---')

    b = board_vuota()
    b[0][7] = 'k'   # re nero in h8
    b[0][0] = 'R'   # torre bianca in a8: scacco sull'ottava
    b[1][0] = 'R'   # torre bianca in a7: toglie la settima
    b[7][4] = 'K'
    print('matto di scala   -> matto:', scacco_matto(b, False),
          ' stallo:', stallo(b, False))

    b = board_vuota()
    b[0][0] = 'k'   # re nero in a8
    b[1][2] = 'Q'   # donna bianca in c7
    b[7][4] = 'K'
    print('re nero in a8, donna bianca in c7 -> matto:', scacco_matto(b, False),
          ' stallo:', stallo(b, False))

    print()
    print('--- promozione ---')

    b = board_vuota()
    b[1][0] = 'P'   # pedone bianco in a7
    b[7][4] = 'K'
    b[0][7] = 'k'
    print('mosse del pedone bianco in a7:', elenco(mosse_legali(b, (1, 0))))

    muovi(b, (1, 0), (0, 0, 'N'))
    print('promuovendo a cavallo, in a8 compare:', b[0][0])

    print()
    print('--- en passant ---')

    p = partita_iniziale()
    esegui_mossa(p, (6, 4), (4, 4))   # 1. e4
    esegui_mossa(p, (1, 0), (3, 0))   # 1... a5
    esegui_mossa(p, (4, 4), (3, 4))   # 2. e5
    esegui_mossa(p, (1, 3), (3, 3))   # 2... d5, doppio passo accanto a e5
    print('il nero ha appena giocato d5, casella di en passant:',
          nome_casella(p['en_passant']))
    print('mosse del pedone bianco in e5:', elenco(mosse_del_pezzo(p, (3, 4))))

    esegui_mossa(p, (3, 4), (2, 3))   # 3. exd6 en passant
    print('dopo exd6, il pedone nero in d5 e\' ancora li\'?',
          p['board'][3][3] != '.')

    print()
    print('--- arrocco ---')

    b = board_vuota()
    b[7][4] = 'K'   # re bianco in e1
    b[7][0] = 'R'   # torre bianca in a1
    b[7][7] = 'R'   # torre bianca in h1
    b[0][4] = 'k'
    diritti = {'K': True, 'Q': True, 'k': True, 'q': True}
    print('re e1 con entrambe le torri:',
          elenco(mosse_legali(b, (7, 4), None, diritti)))

    b[0][5] = 'r'   # torre nera in f8: tiene sotto tiro la colonna f
    print('   ...con una torre nera che controlla la colonna f:',
          elenco(mosse_legali(b, (7, 4), None, diritti)))

    b[0][5] = '.'
    diritti_persi = {'K': False, 'Q': True, 'k': True, 'q': True}
    print('   ...dopo che la torre in h1 si e\' mossa:',
          elenco(mosse_legali(b, (7, 4), None, diritti_persi)))

    p = partita_iniziale()
    for mossa in [((6, 4), (4, 4)), ((1, 4), (3, 4)),      # e4 e5
                  ((7, 6), (5, 5)), ((0, 6), (2, 5)),      # Cf3 Cf6
                  ((7, 5), (4, 2)), ((0, 5), (3, 2))]:     # Ac4 Ac5
        esegui_mossa(p, mossa[0], mossa[1])
    print('partita vera, il bianco ora puo\' arroccare:',
          elenco(mosse_del_pezzo(p, (7, 4))))
    esegui_mossa(p, (7, 4), (7, 6))
    print('dopo l\'arrocco corto:')
    stampa(p['board'])


# questo blocco parte solo se lancio "python scacchiera.py".
# se invece un altro file fa "import scacchiera", non stampa niente:
# senza questa riga ogni import sputerebbe fuori tutte le prove
if __name__ == '__main__':
    prove()
