from cmath import sqrt
from termcolor import colored
import random

class Node():
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent

class Stack():
    def __init__(self, item):
        self.stack = [item] if item else []
    
    def push(self, node):
        self.stack.append(node)
    
    def peek(self):
        return self.stack[-1]
    
    def pop(self):
        '''Returns and removes a node from the stack's last place.'''
        node = self.stack[-1]
        self.stack.remove(node)
        return node 
    
    def isEmpty(self):
        return len(self.stack) == 0

    def contains(self, node):
        return True if node in self.stack else False
    
    def items(self):
        return self.stack

class Queue(Stack):
    def pop(self):
        '''Returns and removes a node from the queue's first place.'''
        node = self.stack[0]
        self.stack.remove(node)
        return node

class Maze():
    def __init__(self, filename):
        self.filename = filename
        self.map = self.loadMap()

    def loadMap(self):
        '''Loads map from a file.'''
        with open(self.filename) as file:
            return file.read().split('\n')
        
    def showMap(self, path, onlyMainPath):
        '''Shows map visually in CLI.'''
        if not path == None:
            for step in path[1:-1]:
                self.map[step[0]] = self.map[step[0]][:step[1]] + '^' + self.map[step[0]][step[1]+1:]
        
        if onlyMainPath:
            print('\n'.join(self.map).replace('#', '█').replace('*', ' ').replace('^', colored('•', "green")))
        else:
            print('\n'.join(self.map).replace('#', '█').replace('*', colored('•', "red")).replace('^', colored('•', "green")))
    
    def getSpots(self):
        '''Returns a tuple with coords of the start and goal spot.'''
        start = None
        goal = None

        for layer in self.map:
            if 'S' in layer:
                start = (self.map.index(layer), layer.index('S'))
        
            if 'G' in layer:
                goal = (self.map.index(layer), layer.index('G'))
    
        return start, goal
    
    def getPossibleStates(self, node):
        '''Returns a list with of all possible neighbour states based on a passed state.'''
        row, col = node.state
        states = []

        if self.map[row][col-1] == ' ' or self.map[row][col-1] == 'G':
            states.append((row, col-1))
        
        if self.map[row][col+1] == ' ' or self.map[row][col+1] == 'G':
            states.append((row, col+1))

        if self.map[row-1][col] == ' ' or self.map[row-1][col] == 'G':
            states.append((row-1, col))
    
        if self.map[row+1][col] == ' ' or self.map[row+1][col] == 'G':
            states.append((row+1, col))
    
        random.shuffle(states)
        return states
    
    def fill(self, node):
        '''Marks explored state with a * sign on maze map.'''
        row, col = node.state
        lst = list(self.map[row])
        lst[col] = '*' if lst[col] == ' ' else lst[col]
        self.map = self.map[:row] + [''.join(lst)] + self.map[row + 1:]

    def getPath(self, node):
        '''Returns a list of of all previous steps that are on a goal path.'''
        if node.parent == None:
            return [node.state]
        else:
            return [node.state] + self.getPath(node.parent)

    def getManhattanDistance(self, *args):
        '''Returns Manhattan distance between two spots.'''
        start, goal = self.getSpots()
        if args[0] != None:
            start = args[0].state
        if args[1] != None:
            goal = args[1].state

        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])
    
    def getEuclideanDistance(self, *args):
        '''Returns Euclidean distance between two spots.'''
        start, goal = self.getSpots()
        if args[0] != None:
            start = args[0].state
        if args[1] != None:
            goal = args[1].state
        # sqrt() returns a complex number (x + yi). 
        # .real returns a real part, and .imag returns a imaginary part of the complex number
        return sqrt((start[0] - goal[0])**2 + (start[1] - goal[1])**2).real