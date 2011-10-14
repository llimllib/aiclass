import random
import heapq
from collections import namedtuple
from romania import graph, straight_line_distance

class FifteenBlocksProblem(object):
    def __init__(self, initial):
        self.initial = initial
        self.goalstate = range(15) + [-1]

    #board is a 16-element list of integers with -1 representing the "hole"
    def actions(self, board):
        idx = board.index(-1)

        moves = ["left", "right", "up", "down"]

        if idx in (3,7,11,15):
            moves.remove("left")
        if idx in (0,4,8,12):
            moves.remove("right")
        if idx in (12,13,14,15):
            moves.remove("up")
        if idx in (0,1,2,3):
            moves.remove("down")

        return moves

    def result(self, board, action):
        """move a piece *action* into the hole

        that is, if action is "up", and the lower right corner looks like:

        1 -1
        3 2

        move the 2 up by swapping 2 and -1"""
        #copy the board
        board = board[:]

        #find the hole
        idx = board.index(-1)

        if action == "left":
            assert idx not in (3,7,11,15)
            board[idx], board[idx+1] = board[idx+1], board[idx]
        elif action == "right":
            assert idx not in (0,4,8,12)
            board[idx], board[idx-1] = board[idx-1], board[idx]
        elif action == "up":
            assert idx not in (12,13,14,15)
            board[idx], board[idx+4] = board[idx+4], board[idx]
        elif action == "down":
            assert idx not in (0,1,2,3)
            board[idx], board[idx-4] = board[idx-4], board[idx]

        return board

    def goaltest(self, board):
        return board == self.goalstate

    def pathcost(self, path):
        pass

    @staticmethod
    def printboard(board):
        print "\t".join(map(str, board[0:4]))
        print "\t".join(map(str, board[4:8]))
        print "\t".join(map(str, board[8:12]))
        print "\t".join(map(str, board[12:16]))

class FifteenBlocksNumberHeuristic(FifteenBlocksProblem):
    def pathcost(self, path):
        #g is the number of moves taken to get to this path
        g = len(path)

        #h is the number of positions in the most recent state that differ
        #from the goal state
        pairs = zip(path[-1], self.goalstate)
        h = sum(1 for a,b in pairs if a!=b)

        return g + h

class FifteenBlocksDistanceHeuristic(FifteenBlocksProblem):
    def pathcost(self, path):
        #g is the number of moves taken to get to this path
        g = len(path)

        #h is the total manhattan distance from the solution
        h = 0

        pairs = zip(path[-1], range(16))
        for a,b in pairs:
            if a == -1: continue

            rowa, cola = divmod(a, 4)
            rowb, colb = divmod(b, 4)
            h += abs(rowa-rowb) + abs(cola-colb)

        return g + h

#define a path class. priority is a positive integer, path is a list of boards
Pathnode = namedtuple('Pathnode', ['priority', 'path'])

def graph_search(problem):
    initialpath = Pathnode(0, [problem.initial])

    #frontier is a heap; we'll maintain it using heapq methods. Norvig suggests maintaining
    #a parallel set of paths for membership testing, but I don't see where it would be useful.
    frontier = [initialpath]

    explored = set()

    while 1:
        if not frontier: return False

        pathnode = heapq.heappop(frontier)
        s = pathnode.path[-1]

        explored.add(tuple(s))

        if problem.goaltest(s):
            return pathnode.path

        for action in problem.actions(s):
            newboard = problem.result(s, action)
            if not tuple(newboard) in explored:
                #we have a new board. Create a path:
                newpath = pathnode.path + [newboard]

                #calculate its cost
                pathcost = problem.pathcost(newpath)

                #now push it onto the priority queue
                heapq.heappush(frontier, Pathnode(pathcost, newpath))

def randomboard(n):
    """Make *n* valid moves to shuffle the board

    Wiki tells us:

        Johnson & Story (1879) used a parity argument to show that half of the
        starting positions for the n-puzzle are impossible to resolve, no
        matter how many moves are made.

    So let's shuffle to assure that the board can be solved"""

    board = range(15) + [-1]
    p = FifteenBlocksProblem(board)

    for i in range(n):
        move = random.choice(p.actions(board))
        board = p.result(board, move)
    
    return board

def main():
    #blocks = FifteenBlocksDistanceHeuristic(randomboard(200))
    blocks = FifteenBlocksDistanceHeuristic([-1, 0, 1, 2, 3, 4, 5, 14, 9, 6, 11, 7, 12, 8, 13, 10])
    print "done shuffling"
    result = graph_search(blocks)
    for board in result:
        FifteenBlocksProblem.printboard(board)
        print

if __name__=="__main__":
    import cProfile
    cProfile.run('main()')
    #main()

"""here's our test case:
[-1, 0, 1, 2, 3, 4, 5, 14, 9, 6, 11, 7, 12, 8, 13, 10]
"""
