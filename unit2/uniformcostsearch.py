import random
from romania import graph

initial = ("Arad", 0)

def tree_search(problem, remove_choice):
    #frontier is a list containing a single array, [initial]
    frontier = [[initial]]
    explored = set()

    while 1:
        if not frontier: return False

        path = remove_choice(frontier)
        s = path[-1]
        city, cost = s

        explored.add(city)

        #if s is a goal, return path
        if city == "Bucharest":
            return (path, frontier)

        #for a in actions
        for node in graph[city]:
            ncity, ncost = node
            if not ncity in explored:
                frontier.append(path + [node])

def cheapest_first(frontier):
    cheapest = 9999999999
    cheapest_path = None
    for i, path in enumerate(frontier):
        pathcost = sum(cost for city, cost in path)
        if pathcost < cheapest:
            cheapest = pathcost
            cheapest_path = i

    return frontier.pop(cheapest_path)

if __name__=="__main__":
    #print "random search: ", tree_search(None, random_choice)[0]
    print "ucs: ", tree_search(None, cheapest_first)
