import sys
import copy
import time
import math
from types import NoneType
# Util module
from util import *  

def show(searchMethod, data):
    print(f"\n{searchMethod.upper()} ----------------------------------\n")
    data[0].showMap(data[1], False)
    print(f"Min steps from S to G is {data[2]}")
    print(f"Steps taken: {data[3]}")
    print(f"Time: {data[4]}s\n")

        
def bfs_search(maze):
    startTime = time.process_time()
    mazeCopy = copy.deepcopy(maze)
    start, goal = mazeCopy.getSpots()

    queue = Queue(Node(start, None))
    switch = True
    steps = 0

    while switch:
        node = queue.pop()
        steps += 1

        for possibleState in mazeCopy.getPossibleStates(node):
            newNode = Node(possibleState, node)
            mazeCopy.fill(newNode)
            queue.push(newNode)
            if newNode.state == goal:
                switch = False
                path = mazeCopy.getPath(newNode)
                minSteps = len(path)
                stepsTaken = steps
                timeTaken = time.process_time() - startTime
                return mazeCopy, path, minSteps, stepsTaken, timeTaken
    

def dfs_search(maze):
    startTime = time.process_time()
    mazeCopy = copy.deepcopy(maze)
    start, goal = mazeCopy.getSpots()
    explored = []

    def dfs(node):
        if node not in explored:
            explored.append(node.state)
            mazeCopy.fill(node)
            if node.state == goal:
                return mazeCopy.getPath(node)
                
            for possibleState in mazeCopy.getPossibleStates(node):
                newNode = Node(possibleState, node)
                if newNode not in explored:
                    path = dfs(newNode)
                    if path:
                        return path
        
        return []            

    path = dfs(Node(start, None))
    minSteps = len(path)
    stepsTaken = len(explored) - 1
    timeTaken = time.process_time() - startTime

    return mazeCopy, path, minSteps, stepsTaken, timeTaken


def a_star_search(maze):
    startTime = time.process_time()
    mazeCopy = copy.deepcopy(maze)
    start, goal = mazeCopy.getSpots()
    explored = []
    waiting = []
    
    def h(node):
        return mazeCopy.getManhattanDistance(node, None)
    
    def a_star(node, currentStepValue, steps):
        explored.append(node.state)
        mazeCopy.fill(node)
        possibleStates = mazeCopy.getPossibleStates(node)
        nextNode = None
        nextStepValue = 0
        
        for possibleState in possibleStates:
            newNode = Node(possibleState, node)
            nextStepValue = h(newNode) + steps + 1
            waiting.append((newNode, steps + 1))
            if nextStepValue <= currentStepValue and h(newNode) <= h(newNode.parent) and newNode.state not in explored:
                nextNode = newNode
        

        if nextNode == None:

            waitingNodes = [wn for wn in waiting if wn[0].state not in explored]
            waitingNodes = sorted(waitingNodes, key=lambda wn: (h(wn[0]) + wn[1], h(wn[0])))

            if waitingNodes:
                return a_star(waitingNodes[0][0], h(waitingNodes[0][0]) + waitingNodes[0][1], waitingNodes[0][1])

            else:
                possibleStates = [state for state in possibleStates if state not in explored]
                if len(possibleStates) == 1:
                    nextNode = Node(possibleStates[0], None)
                    nextStepValue = h(newNode) + steps + 1
                
                return []
        else:
            if nextNode.state == goal:
                return mazeCopy.getPath(nextNode)
        
        return a_star(nextNode, nextStepValue, steps + 1)
          

    startNode = Node(start, None)
    currentStepValue = h(startNode)
    path = a_star(startNode, currentStepValue, 0)
    minSteps = len(path)
    stepsTaken = len(explored) - 1
    timeTaken = time.process_time() - startTime

    return mazeCopy, path, minSteps, stepsTaken, timeTaken
    


maze = Maze(sys.argv[1])
show("bfs", bfs_search(maze))
show("dfs", dfs_search(maze))
show("a*", a_star_search(maze))
