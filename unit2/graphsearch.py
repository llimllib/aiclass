import random
from romania import graph

initial = "Arad"

def tree_search(problem, remove_choice):
    #frontier is a list containing a single array, [initial]
    frontier = [[initial]]
    explored = set()

    while 1:
        if not frontier: return False

        path = remove_choice(frontier)
        s = path[-1]

        explored.add(s)

        #if s is a goal, return path
        if s == "Bucharest":
            return (path, frontier)

        #for a in actions
        for city, _ in graph[s]:
            if not city in explored:
                frontier.append(path + [city])

def random_choice(frontier):
    return frontier.pop(random.randrange(0, len(frontier)))

def first_choice(frontier):
    return frontier.pop(0)

def last_choice(frontier):
    return frontier.pop(-1)

if __name__=="__main__":
    #print "random search: ", tree_search(None, random_choice)[0]
    print "bfs: ", tree_search(None, first_choice)
    print "dfs: ", tree_search(None, last_choice)
