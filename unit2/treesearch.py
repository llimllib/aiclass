import random
from romania import graph

initial = "Arad"

def tree_search(problem, remove_choice):
    #frontier is a list containing a single array, [initial]
    frontier = [[initial]]

    while 1:
        if not frontier: return False

        path = remove_choice(frontier)
        s = path[-1]

        #if s is a goal, return path
        if s == "Bucharest":
            return (path, frontier)

        #for a in actions
        for city, _ in graph[s]:
            frontier.append(path + [city])

def random_choice(frontier):
    return frontier.pop(random.randrange(0, len(frontier)))

def first_choice(frontier):
    return frontier.pop(0)

def last_choice(frontier):
    return frontier.pop(-1)

if __name__=="__main__":
    print "random search (no memory):", tree_search(None, random_choice)[0]
