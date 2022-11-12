import minimax
import time
import concurrent.futures #threading

dir = [[ 0, 1],
       [ 1, 0],
       [ 1, 1],
       [ 1,-1]]

class Board():
    def __init__(self, dim, players, difficulty):
        #self.game = game
        self.dim = dim
        self.players = players
        self.difficulty = difficulty
        self.win = -1
        self.turn = 0

        self.board = []
        self.scores = [0, 0]
        self.nearSquares = set()
        self.count = [0]
        self.ai_score = 0
        self.lastMove = [-1, -1]
        self.pieces = 0
        self.sequences = [
            [[],[],[],[],[]],
            [[],[],[],[],[]]
                           ]

        self.playerSymbol = ['X','O']
        self.EMPTY = "="

        #Board init
        for i in range(0, self.dim):
            self.board.append([])
            for j in range(0, self.dim):
                self.board[i].append(self.EMPTY)

    def move(self, row, col):
        self.sequences = [[[],[],[],[],[]],
                          [[],[],[],[],[]]]
        if(self.board[row][col] == self.EMPTY):
            self.board[row][col] = self.playerSymbol[self.turn]

            self.lastMove = [row, col]

            self.checkMove(row, col)
            if(self.win == -1):
                self.turn = (self.turn + 1)%2

            self.pieces += 1

            self.updateNearSquares(row, col)
            self.checkSequences1(0)
            self.checkSequences1(1)
            self.get_score()



    def checkMove(self, row, col):
        # Per tutte le direzioni
        for d in range(4):
            cnt = 1 #Quante caselle hanno la pedina voluta

            # Controllo quelle a destra (come gia scelte)
            for i in range(1, 5):
                pos_row = row + i*dir[d][0]
                pos_col = col + i*dir[d][1]
                if(self.isInBoard(pos_row, pos_col)):
                    currentPos = self.board[ pos_row ][ pos_col ]
                    if(currentPos == self.board[row][col]):
                        cnt += 1
                    else:
                        break
                else:
                    break

            # Controllo quelle a sinistra
            for i in range(1, 5):
                pos_row = row - i*dir[d][0]
                pos_col = col - i*dir[d][1]
                if(self.isInBoard(pos_row, pos_col)):
                    currentPos = self.board[ pos_row ][ pos_col ]
                    if(currentPos == self.board[row][col]):
                        cnt += 1
                    else:
                        break
                else:
                    break

            if(cnt >= 5):
                self.win = self.turn

        return 0


    def getNearSquares(self):
        return list(self.nearSquares)

    def updateNearSquares(self, row, col):
        if (row, col) in self.nearSquares:
            self.nearSquares.discard((row, col))

        for d in range(len(dir)):
            r,c = row + dir[d][0], col + dir[d][1]
            if self.isInBoard(r,c) and self.board[r][c] == self.EMPTY:
                self.nearSquares.add((r,c))

            r, c = row - dir[d][0], col - dir[d][1]
            if self.isInBoard(r, c) and self.board[r][c] == self.EMPTY:
                self.nearSquares.add((r, c))

    def moveIsAlone(self, row, col):
        alone = 1
        pos = [row, col]

        for i in range(4):
            curr_pos = [row+dir[i][0], col+dir[i][1]]
            if(self.isInBoard(curr_pos[0], curr_pos[1])):
                if(self.board[curr_pos[0]][curr_pos[1]] != self.EMPTY):
                    alone = 0
                    break

            curr_pos = [row-dir[i][0], col-dir[i][1]]
            if(self.isInBoard(curr_pos[0], curr_pos[1])):
                if(self.board[curr_pos[0]][curr_pos[1]] != self.EMPTY):
                    alone = 0
                    break

        return alone

    def checkSequences1(self, player):
        playerColor = self.playerSymbol[player]
        othersColor = self.playerSymbol[(player+1)%2]

        for square in self.nearSquares:
            for d in range(4):
                cnt = 0
                listOfEmpty = [square]
                leftOpen = 0
                rightOpen = 0

                #Check position
                goRight = False
                squareRIGHT = [square[0] + dir[d][0], square[1] + dir[d][1]]
                if(self.isInBoard(squareRIGHT[0], squareRIGHT[1])):
                    if(self.board[squareRIGHT[0]][squareRIGHT[1]] == playerColor):
                        cnt += 1
                        goRight = True

                goLeft = False
                squareLEFT = [square[0] - dir[d][0], square[1] - dir[d][1]]
                if(self.isInBoard(squareLEFT[0], squareLEFT[1])):
                    if(self.board[squareLEFT[0]][squareLEFT[1]] == playerColor):
                        cnt += 1
                        goLeft = True

                isMiddle = goLeft and goRight

                #Check sequence
                if(goLeft):           #---> GO TO LEFT
                    if(not(isMiddle)): #Se non e` un MIDDLE
                        rightOpen = 1

                    for i in range(2,6):
                        currentSquare = [square[0] - i*dir[d][0], square[1] - i*dir[d][1]]
                        if(self.isInBoard(currentSquare[0],currentSquare[1])):
                            if(self.board[currentSquare[0]][currentSquare[1]] == playerColor):
                                cnt += 1
                            elif(self.board[currentSquare[0]][currentSquare[1]] == self.EMPTY):
                                leftOpen = 1
                                if(not(isMiddle)): #Se non e` un MIDDLE
                                    listOfEmpty.append( (currentSquare[0], currentSquare[1]) )
                                break
                            else:
                                break
                        else:
                            break

                if(goRight):          #---> GO TO RIGHT
                    if(not(isMiddle)): #Se non e` un MIDDLE
                        leftOpen = 1
                    for i in range(2,6):
                        currentSquare = [square[0] + i*dir[d][0], square[1] + i*dir[d][1]]
                        if(self.isInBoard(currentSquare[0],currentSquare[1])):
                            if(self.board[currentSquare[0]][currentSquare[1]] == playerColor):
                                cnt += 1
                            elif(self.board[currentSquare[0]][currentSquare[1]] == self.EMPTY):
                                rightOpen = 1
                                if(not(isMiddle)): #Se non e` un MIDDLE
                                    listOfEmpty.append( (currentSquare[0], currentSquare[1]) )
                                break
                            else:
                                break
                        else:
                            break

                self.checkSequence(cnt, listOfEmpty, (rightOpen+leftOpen), player)


    def checkSequence(self, cnt, listOfEmpty, openEnds, player):
        duplicate = 0
        l = len(listOfEmpty)
        if cnt == 0 or cnt > 5:
            return
        for seq in self.sequences[player][cnt-1]:
            duplicate = 1
            if(len(seq['emptySquares']) == l):
                for square in seq['emptySquares']:
                    if not(square in listOfEmpty):
                        duplicate = 0
                        break

                if(duplicate == 1):
                    return

        self.sequences[player][cnt-1].append({'cnt': cnt,
                                                  'openEnds': openEnds,
                                                  'emptySquares': [x for x in listOfEmpty]})


    def isInBoard(self, row, col):
        if(row >= 0 and row < self.dim):
            if(col >= 0 and col < self.dim):
                return 1
        return 0

    def get_score(self):

        playerTurn = self.turn
        othersTurn = (playerTurn+1)%2
        self.scores = [0, 0]
        #Open ends    1     >1
        score = [[[ 0.5,     1],  # cnt == 1      #Se è il proprio turno
                  [   2,     5],  # cnt == 2
                  [  13,  1000],  # cnt == 3
                  [3000, 10000]],   # cnt == 4

                 [[0.5,    1], # cnt == 1      #Se non è il proprio turno
                  [  2,    5],  # cnt == 2
                  [  7, 100],  # cnt == 3
                  [ 8, 5000]]]   # cnt == 4


        for s in range(4):
            for seq in self.sequences[playerTurn][s]:
                if(len(seq['emptySquares']) == 1):
                    self.scores[playerTurn] += score[0][s][0]
                else:
                    self.scores[playerTurn] += score[0][s][1]

        for s in range(4):
            for seq in self.sequences[othersTurn][s]:
                if(len(seq['emptySquares']) == 1):
                    self.scores[othersTurn] += score[1][s][0]
                else:
                    self.scores[othersTurn] += score[1][s][1]

        self.ai_score = self.scores[1] - self.scores[0] - 5*self.pieces



    def getAiMove(self, game):
        self.count = [0]
        game.move_time = 0

        #Start the thread
        #While minimax is thinking
        # move = minimax.minimax(self, self.difficulty, float('-inf'), float('inf'), True, self.count)[1]
        timer = game.time
        with concurrent.futures.ThreadPoolExecutor() as executor:
            minimax_thread = executor.submit(minimax.minimax,  #func
                                            self, self.difficulty, self.difficulty, float('-inf'), float('inf'), True, self.count) #args

            while(minimax_thread.running()):
                game.update_window()
                game.move_time = game.time - timer


        move = minimax_thread.result()[1]
        self.move(move[0], move[1])


