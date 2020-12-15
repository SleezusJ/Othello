import random


# this class stores an othello board state
# the state is handled as a 1d list that stores a 10x10 board.  1 and -1 are the two colors, 0 are empty squares
class Board:
    # make a starting board.  There are four pieces in the center
    def __init__(self):
        self.state = [0] * 100
        self.state[44] = 1
        self.state[45] = -1
        self.state[54] = -1
        self.state[55] = 1

    # returns the score as the difference between the number of 1s and the number of -1s
    def evaluate(self):
        value = 0
        for i in range(100):
            if self.state[i] == 1:
                value = value + 1
            elif self.state[i] == -1:
                value = value - 1
        return value


    # # gets score of a given move
    # def score(self, player: int):
    #     # remember how to quantify move score...
    #     if player == 1:
    #         return self.evaluate()
    #     elif player == -1:
    #         return -self.evaluate()


    # returns a new board that is a copy of the current board
    def copy(self):
        board = Board()
        for i in range(100):
            board.state[i] = self.state[i]
        return board

    # given a x,y position, returns the tile within the 1d list
    def index(self, x, y):
        if x >= 0 and x < 10 and y >= 0 and y < 10:
            return self.state[x + y * 10]
        else:
            # out of bounds, return -2 for error
            return -2

    # given an x,y coordinate, and an id of 1 or -1, returns true if this is a valid move
    def canplace(self, x, y, id):
        # square is not empty? return false
        if self.index(x, y) != 0:
            return False
        # these functions compute the 8 different directions
        dirs = [(lambda x: x, lambda y: y - 1), (lambda x: x, lambda y: y + 1), (lambda x: x - 1, lambda y: y - 1),
                (lambda x: x - 1, lambda y: y), (lambda x: x - 1, lambda y: y + 1), (lambda x: x + 1, lambda y: y - 1),
                (lambda x: x + 1, lambda y: y), (lambda x: x + 1, lambda y: y + 1)]
        # for each direction...
        for xop, yop in dirs:
            # move one space.  is the piece the opponent's color?
            i, j = xop(x), yop(y)
            if self.index(i, j) != -id:
                # no, then we'll move on to the next direction
                continue
            # keep going until we hit our own piece
            i, j = xop(i), yop(j)
            while self.index(i, j) == -id:
                i, j = xop(i), yop(j)
            # if we found a piece of our own color, then this is a valid move
            if self.index(i, j) == id:
                return True
        # if I can't capture in any direction, I can't place here
        return False

    # given an x,y coordinate, and an id of 1 or -1, place a tile (if valid) at x,y, and modify the state accordingly
    def place(self, x, y, id):
        # don't bother if it isn't a valid move
        if not self.canplace(x, y, id):
            return
        # place your piece at x,y
        self.state[x + y * 10] = id
        dirs = [(lambda x: x, lambda y: y - 1), (lambda x: x, lambda y: y + 1), (lambda x: x - 1, lambda y: y - 1),
                (lambda x: x - 1, lambda y: y), (lambda x: x - 1, lambda y: y + 1), (lambda x: x + 1, lambda y: y - 1),
                (lambda x: x + 1, lambda y: y), (lambda x: x + 1, lambda y: y + 1)]
        # go through each direction
        for xop, yop in dirs:
            i, j = xop(x), yop(y)
            # move one space.  is the piece the opponent's color?
            if self.index(i, j) != -id:
                # no, then we can't capture in this direction.  we'll move on to the next one
                continue
            # keep going until we hit our own piece
            while self.index(i, j) == -id:
                i, j = xop(i), yop(j)
            # if we found a piece of our own color, then this is a valid move
            if self.index(i, j) == id:
                k, l = xop(x), yop(y)
                # go back and flip all the pieces to my color
                while k != i or l != j:
                    self.state[k + l * 10] = id
                    k, l = xop(k), yop(l)

    # returns a list of all valid x,y moves for a given id
    def validmoves(self, id):
        moves = []
        for x in range(10):
            for y in range(10):
                if self.canplace(x, y, id):
                    moves = moves + [(x, y)]
        return moves

    # print out the board.  1 is X, -1 is O
    def printboard(self):
        for y in range(10):
            line = ""
            for x in range(10):
                if self.index(x, y) == 1:
                    line = line + "X"
                elif self.index(x, y) == -1:
                    line = line + "O"
                else:
                    line = line + "."
            print(line)

    # state is an end game if there are no empty places
    def end(self):
        return not 0 in self.state


def allmoves(board, player):
    children = []
    for move in board.validmoves(player):
        child = board.copy()
        child.place(move[0], move[1], player)
        children.append(child)
    return children


# gets score of a given move
def score(move: Board, player: int):
    # remember how to quantify move score...
    if player == 1:
        return move.evaluate()
    elif player == -1:
        return -move.evaluate()


def greedy(board: Board, player: int):
    moves = allmoves(board, player)
    # rank the moves: every move has a score with it
    for m in range(len(moves)):
        # transform each move into a (score,move)
        #moves[m] = (board.score(moves[m], player), moves[m])
        moves[m] = (score(moves[m], player), moves[m])
    # sort them so good moves up front
    moves.sort(reverse=True, key=lambda x: x[0])

    if not moves[0][0]:
        return None

    # make a sublist of the top group
    # let's get the best score (score of first one)
    topscore = moves[0][0]
    # move forward until stop seeing that score
    index = 0
    while index < len(moves) and moves[index][0] == topscore:
        index += 1
    moves = moves[:index]
    # pick one randomly from the best moves
    move = moves[random.randrange(0, len(moves))]
    # remove the score
    move = move[1]
    return move


# looks at all my moves, looks at countermoves
def minimax_oneply(brd,player):
    # get my moves
    moves = allmoves(brd, player)
    # rank the moves: assign a score
    for m in range(len(moves)):
        #if not tied, put in the score
        if score(moves[m],player) != 0:
            moves[m] = (score(moves[m], player), moves[m])
        else:
            # if game is unfinished, let's look at countermoves
            counter = allmoves(moves[m], -player)
            # let's score and rank these counter moves
            # putting a score at front of each counter-move
            for c in range(len(counter)):
                counter[c] = (score(counter[c], player), counter[c])
            # rank them, with the worst first
            counter.sort(reverse=False, key=lambda x: x[0])
            #print(counter)
            # get the value of the worst countermove score
            minscore = counter[0][0]
            # use that to score my move
            moves[m] = (minscore,moves[m])

    # we need to take the max of the mins
    moves.sort(reverse=True, key=lambda x: x[0])

    if not moves[0][0]:
        return None

    # make a sublist of the top group
    #let's get the best score (score of first one)
    topscore=moves[0][0]
    #move forward until stop seeing that score
    index=0
    while index<len(moves) and moves[index][0]==topscore:
        index+=1
    moves=moves[:index]
    # pick one randomly from the best moves
    move=moves[random.randrange(0,len(moves))]
    # remove the score
    move=move[1]
    return move


# looks at all my moves, looks at countermoves
def minimax_ndepth(brd, player, depth, toplevel=True):
    # get my moves
    moves = allmoves(brd, player)
    # rank the moves: assign a score
    for m in range(len(moves)):
        #if not tied, put in the score
        if score(moves[m],player) != 0:
            moves[m] = (score(moves[m], player), moves[m])
        else:
            # look at countermoves
            counter = allmoves(moves[m], -player)
            # score and rank these counter moves
            # make score - counter move tuple
            for c in range(len(counter)):
                #counter[c] = (score(counter[c], player), counter[c])
                # if countermove is endgame,
                if counter[c].end():
                    counter[c] = (score(counter[c], player), counter[c])
                elif len(counter[c].validmoves(-player)) == 0:
                    counter[c] = (score(counter[c], player), counter[c])
                elif depth == 0:
                    counter[c] = (score(counter[c], player), counter[c])
                else:
                    counter[c] = minimax_ndepth(counter[c], player, (depth-1), False)
            # rank them, with the worst first
            counter.sort(reverse=False, key=lambda x: x[0])
            # get the value of the worst countermove score
            minscore = counter[0][0]
            # use that to score my move
            moves[m] = (minscore,moves[m])

    moves.sort(reverse=False, key=lambda x: x[0])
    if toplevel == False:
        return moves[0][0]
    else:
        if not moves[0][0]:
            return None

        # make a sublist of the top group
        # let's get the best score (score of first one)
        topscore = moves[0][0]
        # move forward until stop seeing that score
        index = 0
        while index < len(moves) and moves[index][0] == topscore:
            index += 1
        moves = moves[:index]
        # pick one randomly from the best moves
        move = moves[random.randrange(0, len(moves))]
        # remove the score
        move = move[1]
        return move


def game():
    # make the starting board
    board = Board()
    # start with player 1
    turn = 1
    while True:
        if turn == 1:
            print("X's Turn: ")
        elif turn == -1:
            print("O's Turn: ")
        """
        # this plays a game between two players that will play completely randomly

        # get the moves
        movelist = board.validmoves(turn)
        # no moves, skip the turn
        if len(movelist) == 0:
            turn = -turn
            continue
        # pick a move totally at random
        i = random.randint(0, len(movelist) - 1)
        # make a new board
        board = board.copy()
        # make the move
        board.place(movelist[i][0], movelist[i][1], turn)
        """
        """
        # 2 greedy player
        board = greedy(board, turn)
        """
        if turn == 1:
            board = greedy(board, turn)
        else:
            #board = minimax_oneply(board,turn)
            board = minimax_ndepth(board,turn,2,True)

        if board is None:
            break

        # swap players
        turn = -turn

        # print
        board.printboard()
        # wait for user to press a key
        input()
        # game over? stop.
        if board.end():
            break
    print("Score is", board.evaluate())


game()
