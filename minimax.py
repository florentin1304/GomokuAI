from copy import deepcopy
import time
import random

MAX_WIDTH = 12 # ~15 in general
#TODO: Create an AI object to do memoization

def minimax(board, max_depth, depth, alpha, beta, isMaximizing, count):
    if depth == 0 or board.win != -1:
        count[0] += 1
        return board.ai_score, (0, 0) #il secondo non credo sia giusto

    all_moves = get_all_moves(board, sortRev=True if isMaximizing else False)

    #if len(all_moves) == 1:
    #    print(board.ai_score, all_moves[0])
    #    return board.ai_score, all_moves[0][1]

    if (board.pieces <= 1):
        return 3.5, random.choice(all_moves)[1]

    best_move = None
    if isMaximizing:
        maxEval = float('-inf')
        for m in range(len(all_moves)):
            count[0] += 1
            move = all_moves[m]
            eval = minimax(move[0], max_depth, depth-1, alpha, beta, False, count)[0]
            maxEval= max(maxEval, eval)

            if maxEval == eval:
                best_move = move[1]

            alpha = max(alpha, eval)
            if(beta <= alpha):
                break

        return maxEval, best_move

    else:
        minEval = float('inf')

        for m in range(len(all_moves)):
            count[0] += 1
            move = all_moves[m]
            eval = minimax(move[0], max_depth, depth-1, alpha, beta, True, count)[0]
            minEval = min(minEval, eval)

            if minEval == eval:
                best_move = move[1]

            beta = min(beta, eval)
            if (beta <= alpha):
                break

        return minEval, best_move



def simulate_move(board, move):
    board.move(move[0], move[1])
    return board

def get_all_moves(board, sortRev):
    moves = [] #ha dentro delle liste/tuple (new_board, (row,col) )
    pos_moves = get_noticeable_moves(board)
    # pos_moves = board.nearSquares
    num = len(pos_moves)
    for move in pos_moves:
        temp_board = deepcopy(board)
        initialScore = board.ai_score
        new_board = simulate_move(temp_board, move)
        moves.append([new_board, move, new_board.ai_score - initialScore])


    moves = sorted(moves, key=lambda moves: moves[2], reverse=sortRev)

    return moves[0:(min(num, MAX_WIDTH))]

def get_noticeable_moves(board):
    playerTurn = board.turn
    othersTurn = (playerTurn+1)%2
    noticeableMoves = []

    for seq in board.sequences[playerTurn][4-1]:
        for move in seq['emptySquares']:
            noticeableMoves.append(move)

    if(noticeableMoves == []):
        for seq in board.sequences[othersTurn][4-1]:
            for move in seq['emptySquares']:
                noticeableMoves.append(move)

    if(noticeableMoves == []):
        for seq in board.sequences[playerTurn][3-1]:
            if(seq['openEnds'] > 1):
                for move in seq['emptySquares']:
                    if(move not in noticeableMoves):
                        noticeableMoves.append(move)

    if(noticeableMoves == []):
        for seq in board.sequences[othersTurn][3-1]:
            if(seq['openEnds'] > 1):
                for move in seq['emptySquares']:
                    if(move not in noticeableMoves):
                        noticeableMoves.append(move)

    # if(noticeableMoves == []):
    #     for seq in board.sequences[playerTurn][3-1]:
    #         for move in seq['emptySquares']:
    #             if(move not in noticeableMoves):
    #                 noticeableMoves.append(move)

    # if(noticeableMoves == []):
    #     for seq in board.sequences[othersTurn][3-1]:
    #         for move in seq['emptySquares']:
    #             if(move not in noticeableMoves):
    #                 noticeableMoves.append(move)

    # if(noticeableMoves == []):
    #     for seq in board.sequences[playerTurn][2-1]:
    #         if(len(seq['emptySquares']) > 1):
    #             for move in seq['emptySquares']:
    #                 if(move not in noticeableMoves):
    #                     noticeableMoves.append(move)
    #     for seq in board.sequences[othersTurn][2-1]:
    #         if(len(seq['emptySquares']) > 1):
    #             for move in seq['emptySquares']:
    #                 if(move not in noticeableMoves):
    #                     noticeableMoves.append(move)

    if(noticeableMoves == []):
        noticeableMoves = board.getNearSquares()

    return noticeableMoves
