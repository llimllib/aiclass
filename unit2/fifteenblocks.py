import random
import heapq
from collections import namedtuple
from romania import graph, straight_line_distance
from manhattancache import manhattancache

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

    def pathcost(self, node):
        if node.parent:
            return node.parent.path_cost + 1
        else:
            return 0

class FifteenBlocksNumberHeuristic(FifteenBlocksProblem):
    def h(self, node):
        #h is the number of positions in the most recent state that differ
        #from the goal state
        h = 0
        for i in range(16): 
            if node.state[i] != self.goalstate[i]:
                h += 1
        return h

class FifteenBlocksDistanceHeuristic(FifteenBlocksProblem):
    def h(self, node):
        #h is the total manhattan distance from the solution
        h = 0

        pairs = zip(node.state, range(16))
        for a,b in pairs:
            if a == -1: continue

            h += manhattancache[a][b]

        return h

#the node data structure
Node = namedtuple('Node', ['f', 'path_cost', 'state', 'action', 'parent'])

def graph_search(problem):
    root = Node(0, 0, problem.initial, None, None)

    #frontier is a heap; we'll maintain it using heapq methods. Norvig suggests maintaining
    #a parallel set of nodes for membership testing, but I don't see where it would be useful.
    frontier = [root]

    explored = set()

    while 1:
        if not frontier: return False

        node = heapq.heappop(frontier)
        s = node.state

        explored.add(tuple(s))

        if problem.goaltest(s):
            return node

        for action in problem.actions(s):
            newboard = problem.result(s, action)
            if not tuple(newboard) in explored:
                #we have a new board. Create a path:
                cost = problem.pathcost(node)

                #TODO: NumberHeuristic won't work with this yet. FIXME
                h = problem.h(node)

                child = Node(h + cost, cost, newboard, action, node)

                #now push it onto the priority queue
                heapq.heappush(frontier, child)

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

    print "done shuffling"
    
    return board

def cache_manhattan():
    cache = {}
    for block in range(15):
        cache[block] = {}
        for i in range(16):
            rowa, cola = divmod(block, 4)
            rowb, colb = divmod(i, 4)
            cache[block][i] = abs(rowa-rowb) + abs(cola-colb)
    return cache


def main():
    #blocks = FifteenBlocksDistanceHeuristic(randomboard(2))
    blocks = FifteenBlocksDistanceHeuristic(randomboard(2000))

    #Distance works, number doesn't
    #blocks = FifteenBlocksDistanceHeuristic([-1, 0, 1, 2, 3, 4, 5, 14, 9, 6, 11, 7, 12, 8, 13, 10])
    #blocks = FifteenBlocksNumberHeuristic([-1, 0, 1, 2, 3, 4, 5, 14, 9, 6, 11, 7, 12, 8, 13, 10])

    #here are the tests from http://pyrorobotics.org/?page=PyroModuleAI:Search
    #blocks = FifteenBlocksDistanceHeuristic([4,0,10,6, 8,1,11,3, 12,13,2,9, 7,-1,5,14])
    #blocks = FifteenBlocksDistanceHeuristic([0,1,6,3, 8,4,7,9, 12,14,5,11, 13,-1,2,10])
    #blocks = FifteenBlocksDistanceHeuristic([6,8,3,0, 12,5,4,9, -1,7,2,11, 13,14,1,10])

    result = graph_search(blocks)
    print "result: ", result.state
    #while result.parent:
    #    print "state", result.state
    #    FifteenBlocksProblem.printboard(result.state)
    #    print
    #    result = result.parent

if __name__=="__main__":
    #pypy runs about 15% faster than regular python
    import cProfile
    cProfile.run('main()')
    #main()
