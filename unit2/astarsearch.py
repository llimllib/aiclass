import random
from romania import graph, straight_line_distance

class RomaniaProblem(object):
    def __init__(self, startcity, endcity):
        self.startcity = (startcity, 0)
        self.endcity = endcity

    def actions(self, city):
        return graph[city]

    def goaltest(self, test_city):
        return test_city == self.endcity

    def pathcost(self, path):
        g = sum(cost for city, cost in path)
        lastcity = path[-1][0]
        h = straight_line_distance[lastcity]
        return g + h

def tree_search(problem, remove_choice):
    #frontier is a list containing a single array, [initial]
    frontier = [[problem.startcity]]
    explored = set()

    while 1:
        if not frontier: return False

        path = remove_choice(frontier, problem)
        s = path[-1]
        city, cost = s

        explored.add(city)

        #if s is a goal, return path
        if problem.goaltest(city):
            return (path, frontier)

        #for a in actions
        for node in problem.actions(city):
            ncity, ncost = node
            if not ncity in explored:
                frontier.append(path + [node])

def astar(frontier, problem):
    cheapest = None
    cheapest_path = None

    for i, path in enumerate(frontier):
        pathcost = problem.pathcost(path)
        if not cheapest or pathcost < cheapest:
            cheapest = pathcost
            cheapest_path = i

    return frontier.pop(cheapest_path)

if __name__=="__main__":
    r = RomaniaProblem("Arad", "Bucharest")
    print "astar: ", tree_search(r, astar)
