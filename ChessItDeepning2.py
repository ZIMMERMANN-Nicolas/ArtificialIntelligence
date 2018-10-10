import time
import chess
from random import randint

board = chess.Board()
# print(board)
# moves = [m for m in board.legal_moves]
#
# print("Il y a " + str(len(moves)) + " coups possibles")
# for c in moves:
#     print(c)
#
# board.push(moves[0])
# print(board)
# board.pop()
# print(board)


deadline = 0



def deroulement(b, maxdepth = 10):
    print("----------")
    print(b)
    if maxdepth is 0 or b.is_game_over():
        return
    for move in b.legal_moves:
        b.push(move)
        deroulement(b, maxdepth-1)
        b.pop()

def deroulementRandom(b):
    print("----------")
    print(b)
    if b.is_game_over():
        return
    moves = [m for m in b.legal_moves]
    assert len(moves) > 0
    move = moves[randint(0,len(moves)-1)]
    b.push(move)
    deroulementRandom(b)
    b.pop()

def board2tab(b):
    return [x.split(' ') for x in str(b).split('\n')]

valpieces = {'.':0,'P':1,'R':5,'N':3,'B':3,'Q':9,'K':200}

def evalpiece(p):
    if p == p.upper(): # Blanc
        return valpieces[p]
    else:
        return -valpieces[p.upper()]

def evalBoard(b):
    score = 0
    tab = board2tab(b)
    for l in tab:
        for p in l:
            score += evalpiece(p)
    return score

# Votre code de MiniMax et plus tard Alpha Beta ici

def MinMax(b, depth = 4):
    if depth is 0 or b.is_game_over():
        return evalBoard(b)

    best = -float("inf")

    for m in b.legal_moves:
        b.push(m)
        best = max(best, MaxMin(b, depth - 1))
        b.pop()

    return best

def MaxMin(b, depth = 4):
    if depth is 0 or b.is_game_over():
        return evalBoard(b)

    worst = float("inf")

    for m in b.legal_moves:
        b.push(m)
        worst = min(worst, MinMax(b, depth - 1))
        b.pop()

    return worst

def playMoveMiniMax(b):
    if b.is_game_over():
        return

    best_move = None
    loss = -float("inf")
    depth = 3

    for m in b.legal_moves:
        b.push(m)
        current_loss = MaxMin(b, depth)
        if(loss < current_loss):
            loss = current_loss
            best_move = m
        b.pop()

    b.push(best_move)

def playMoveAlphaBeta(b):
    if b.is_game_over():
        return

    best_move = None
    loss = -float("inf")
    alpha = -float("inf")
    beta = float("inf")
    depth = 4

    for m in b.legal_moves:
        b.push(m)
        current_loss = MinValue(b, depth, alpha, beta)
        if(loss < current_loss):
            loss = current_loss
            best_move = m
        b.pop()

    b.push(best_move)


#Hash--------------------------------------------------------------------------
def initHash(size):
    global table
    table = [[0 for k in range(12)] for k in range(64)]
    for i in range(64):
        for j in range(12):
            table[i][j] = randint(0,2**20)
    global hashTable
    hashTable = [None for k in range(size)]#bestmove, alpha, beta, depth
    

def setHash(value, data):
    value = value % len(hashTable)
    hashTable[value] = data

def getHash(board):
    return hashTable[getHashValue(board)]
    
def getPieceValue(p):
    res = p.piece_type
    if p.color:
        res += 6
    return res

def getHashValue(b):
    hash = 0
    for k in range(64):
        if board.piece_at(k) != None:
            v = getPieceValue(board.piece_at(k))
            hash = hash ^ table[k][v]
    return hash

def getKnownSituation(board, current_depth):
    tmp = getHash(board)
    if tmp != None and tmp[3] >= current_depth:
        return tmp
    
    return None
    
    
#EndHash-----------------------------------------------------------------------

def playMoveAlphaBetaDeepening(b, available_time = 10):
    if b.is_game_over():
        return
    
    global deadline
    init_time = time.time()
    deadline = init_time + available_time
    
    best_move = None
    loss = -float("inf")
    alpha = -float("inf")
    beta = float("inf")
    current_depth = 3

    while(True):
        print(time.time()- init_time)
        try:
            for m in b.legal_moves:
                b.push(m)
                current_loss = MinValue(b, current_depth, alpha, beta)
                if(loss < current_loss):
                    loss = current_loss
                    best_move = m
                b.pop()
            setHash(getHashValue(b), [best_move, alpha, beta, current_depth])
            current_depth += 1
        except RuntimeError:
            b.pop()
            b.push(best_move)
            return


    b.push(best_move)

def MaxValue(b, depth, alpha, beta):
    if depth is 0 or b.is_game_over():
        return evalBoard(b)

    for m in b.legal_moves:
        if(time.time() > deadline):
            raise RuntimeError()
        b.push(m)
        
        try:
            alpha = max(alpha, MinValue(b, depth - 1, alpha, beta))
        except RuntimeError as e:
            b.pop()
            raise e
        if(alpha >= beta):
            b.pop()
            return beta

        b.pop()

    return alpha

def MinValue(b, depth, alpha, beta):
    if depth is 0 or b.is_game_over():
        return evalBoard(b)

    for m in b.legal_moves:
        if(time.time() > deadline):
            raise RuntimeError()
        b.push(m)
        try:
            beta = min(beta, MaxValue(b, depth - 1, alpha, beta))
        except RuntimeError as e:
            b.pop()
            raise e
        if(alpha >= beta):
            b.pop()
            return alpha

        b.pop()

    return beta

def main():
    turn = True#True for white
    while(not board.is_game_over()):
        print(board)
        print("----------")
        if(turn):
            print("White (IA) playing")
            playMoveAlphaBetaDeepening(board)
        else:
            print("Black (random) playing")
            moves = [m for m in board.legal_moves]
            move = moves[randint(0,len(moves)-1)]
            board.push(move)

        turn = not turn

    print("Game ended")
    print(board)
    print("----------")


main()