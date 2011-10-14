import random
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

            #I believe sum(divmod(diff, 4)) will be the manhattan distance
            #between each point and where it should be
            rowa, cola = divmod(a, 4)
            rowb, colb = divmod(b, 4)
            print a, b, abs(rowa-rowb) + abs(cola-colb)
            h += abs(rowa-rowb) + abs(cola-colb)

        print "total distance: ", h, path[-1]

        return g + h

def tree_search(problem, remove_choice):
    frontier = [[problem.initial]]
    explored = set()

    while 1:
        if not frontier: return False

        path = remove_choice(frontier, problem)
        s = path[-1]

        explored.add(tuple(s))

        #if s is a goal, return path
        if problem.goaltest(s):
            return (path, frontier)

        #for a in actions
        for action in problem.actions(s):
            node = problem.result(s, action)
            if not tuple(node) in explored:
                #print "action", action, "results in node", node
                #this implicitly creates a copy of path
                frontier.append(path + [node])

def astar(frontier, problem):
    cheapest = None
    cheapest_path = None

    for i, path in enumerate(frontier):
        pathcost = problem.pathcost(path)
        #print "path", i, path, "has cost", pathcost
        if cheapest is None or pathcost < cheapest:
            #print "setting cheapest to ", i, "with pathcost", pathcost
            cheapest = pathcost
            cheapest_path = i

    #print "choosing path", cheapest_path
    #FifteenBlocksProblem.printboard(frontier[cheapest_path][-1])
    print cheapest

    return frontier.pop(cheapest_path)

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

if __name__=="__main__":
    #blocks = FifteenBlocksNumberHeuristic([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,-1])
    #result = tree_search(blocks, astar)
    #print result

    #blocks = FifteenBlocksNumberHeuristic([0,1,2,3,4,5,6,7,8,9,10,11,12,13,-1,14])
    #result = tree_search(blocks, astar)
    #print result

    #blocks = FifteenBlocksDistanceHeuristic([0,1,2,3,4,5,6,7,8,9,10,11,12,-1,13,14])
    #result = tree_search(blocks, astar)
    #print result

    #blocks = FifteenBlocksNumberHeuristic(randomboard(10))
    #result = tree_search(blocks, astar)
    #print result

    blocks = FifteenBlocksDistanceHeuristic([0, 1, 2, 3, 4, 9, 5, 7, 8, 6, 10, 11, 12, -1, 13, 14])
    result = tree_search(blocks, astar)
    print result

"""Pathological behavior exhibited on:

[0, 1, 2, 3, 4, 9, 5, 7, 8, 6, 10, 11, 12, -1, 13, 14]

Where the solution should be: left, left. WTF?"""
