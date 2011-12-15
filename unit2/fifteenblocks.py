import random
import heapq
import time
from collections import namedtuple
from manhattancache import manhattancache

def swap(tup, idx1, idx2):
    #is there a better way to swap tuple indexes?
    l = list(tup)
    l[idx1], l[idx2] = l[idx2], l[idx1]
    return tuple(l)

class FifteenBlocksProblem(object):
    def __init__(self, initial):
        self.initial = initial
        self.goalstate = tuple(range(15)) + (-1,)

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
        #find the hole
        idx = board.index(-1)

        if action == "left":
            assert idx not in (3,7,11,15)
            return swap(board, idx, idx+1)
        elif action == "right":
            assert idx not in (0,4,8,12)
            return swap(board, idx, idx-1)
        elif action == "up":
            assert idx not in (12,13,14,15)
            return swap(board, idx, idx+4)
        elif action == "down":
            assert idx not in (0,1,2,3)
            return swap(board, idx, idx-4)

    def goaltest(self, board):
        return board == self.goalstate

    def pathcost(self, node):
        if node.parent:
            return node.parent.path_cost + 1
        else:
            return 0

    @staticmethod
    def stringnodes(nodes):
        """turn a list of boards into a string"""
        result = ""
        for node in nodes:
            result += "\t".join(map(str, node.state[0:4])) + "\t|\t"
        result += "\n"
        for node in nodes:
            result += "\t".join(map(str, node.state[4:8])) + "\t|\t"
        result += "\n"
        for node in nodes:
            result += "\t".join(map(str, node.state[8:12])) + "\t|\t"
        result += "\n"
        for node in nodes:
            result += "\t".join(map(str, node.state[12:16])) + "\t|\t"
        result += "\n"
        for node in nodes:
            if node.parent:
                result += "%s\t%s\t%s\t%s\t|\t" % (node.f, node.action, str(id(node))[-5:], str(id(node.parent))[-5:])
            else:
                result += "%s\t%s\t%s\t%s\t|\t" % (node.f, node.action, str(id(node))[-5:], "null")
        result += "\n"

        return result

    @staticmethod
    def printboard(board):
        print "\t".join(map(str, board[0:4]))
        print "\t".join(map(str, board[4:8]))
        print "\t".join(map(str, board[8:12]))
        print "\t".join(map(str, board[12:16]))

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
    def h(self, board):
        #h is the total manhattan distance from the solution
        h = 0

        pairs = zip(board, range(16))
        for a,b in pairs:
            if a == -1: continue

            h += manhattancache[a][b]

        return h

def printtree(frontier):
    out = file("out.html", 'w')
    out.write("<html><body><pre>")
    levels = {}
    already_printed = set()
    for node in frontier:
        while node:
            if node not in already_printed:
                levels.setdefault(node.path_cost, []).append(node)
                already_printed.add(node)
            node = node.parent

    for level in sorted(levels):
        out.write(FifteenBlocksProblem.stringnodes(levels[level]))
        out.write("-------------------------------\n")
    out.write("</pre></body></html>")
    out.close()

#the node data structure
Node = namedtuple('Node', ['f', 'path_cost', 'state', 'action', 'parent'])

def graph_search(problem):
    root = Node(0, 0, problem.initial, None, None)

    #frontier is a heap; we'll maintain it using heapq methods.
    frontier = [root]

    explored = set()

    expanded = 0
    t1 = time.time()

    while 1:
        if not frontier: return False

        node = heapq.heappop(frontier)
        s = node.state

        if problem.goaltest(s):
            return node

        explored.add(s)
        expanded += 1

        if expanded % 100000 == 0:
            t2 = time.time()
            print "%.2fk nodes/sec" % (100/(t2-t1),)
            t1 = time.time()

        for action in problem.actions(s):
            newstate = problem.result(s, action)
            if newstate not in explored:
                cost = node.path_cost + 1

                h = problem.h(newstate)

                child = Node(h + cost, cost, newstate, action, node)

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

def test():
    tests = [
        FifteenBlocksDistanceHeuristic((-1,) + tuple(range(14,-1,-1))),
        #FifteenBlocksDistanceHeuristic((-1, 0, 1, 2, 3, 4, 5, 14, 9, 6, 11, 7, 12, 8, 13, 10)),
        #FifteenBlocksDistanceHeuristic((4,0,10,6, 8,1,11,3, 12,13,2,9, 7,-1,5,14)),
        #FifteenBlocksDistanceHeuristic((0,1,6,3, 8,4,7,9, 12,14,5,11, 13,-1,2,10)),
        #FifteenBlocksDistanceHeuristic((6,8,3,0, 12,5,4,9, -1,7,2,11, 13,14,1,10)),
    ]

    for t in tests:
        print "testing %s" % (t.initial,)
        result = graph_search(t)
        assert result.state == (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,-1)

        pathlen = 0
        while result.parent:
            pathlen += 1
            result = result.parent
        print "%s nodes in solution" % pathlen

        assert pathlen < 81

def main():
    #blocks = FifteenBlocksDistanceHeuristic(randomboard(2))
    #blocks = FifteenBlocksDistanceHeuristic(randomboard(2000))

    #Distance works, number doesn't
    #blocks = FifteenBlocksDistanceHeuristic((-1, 0, 1, 2, 3, 4, 5, 14, 9, 6, 11, 7, 12, 8, 13, 10))
    #blocks = FifteenBlocksNumberHeuristic((-1, 0, 1, 2, 3, 4, 5, 14, 9, 6, 11, 7, 12, 8, 13, 10))

    #here are the tests from http://pyrorobotics.org/?page=PyroModuleAI:Search
    #blocks = FifteenBlocksDistanceHeuristic((4,0,10,6, 8,1,11,3, 12,13,2,9, 7,-1,5,14))
    #blocks = FifteenBlocksDistanceHeuristic((0,1,6,3, 8,4,7,9, 12,14,5,11, 13,-1,2,10))
    blocks = FifteenBlocksDistanceHeuristic((6,8,3,0, 12,5,4,9, -1,7,2,11, 13,14,1,10))

    print "graph: ", blocks.initial
    result = graph_search(blocks)
    print "result: ", result.state
    #while result.parent:
    #    print "state", result.state
    #    FifteenBlocksProblem.printboard(result.state)
    #    print
    #    result = result.parent

if __name__=="__main__":
    #pypy runs about 15% faster than regular python
    #import cProfile
    #cProfile.run('main()')
    #main()
    test()

"""OPEN = priority queue containing START
CLOSED = empty set
while lowest rank in OPEN is not the GOAL:
  current = remove lowest rank item from OPEN
  add current to CLOSED
  for neighbors of current:
    cost = g(current) + movementcost(current, neighbor)
    if neighbor in OPEN and cost less than g(neighbor):
      remove neighbor from OPEN, because new path is better
    if neighbor in CLOSED and cost less than g(neighbor): **
      remove neighbor from CLOSED
    if neighbor not in OPEN and neighbor not in CLOSED:
      set g(neighbor) to cost
      add neighbor to OPEN
      set priority queue rank to g(neighbor) + h(neighbor)
      set neighbor's parent to current

reconstruct reverse path from goal to start
by following parent pointers

from http://11011110.livejournal.com/135302.html, which refs amit patels' a* pages: http://theory.stanford.edu/~amitp/GameProgramming/ImplementationNotes.html

So, do I correctly implement the last bits?
"""
