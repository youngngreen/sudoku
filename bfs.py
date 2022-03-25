from queue import Queue
import copy
import time
import os, psutil
from createBoard import *
from display import *

class Prob(object):

    def __init__(self, initial):
        self.initial = initial
        self.size = len(initial)
        self.height = int(self.size/3)

    def valFil(self, values, used):
        return [number for number in values if number not in used]

    def getSpt(self, board, state):
        for row in range(board):
            for column in range(board):
                if state[row][column] == 0:
                    return row, column   

    def acts(self, state):
        number_set = range(1, self.size+1)
        in_column = []
        in_block = []

        row,column = self.getSpt(self.size, state)

        in_row = [number for number in state[row] if (number != 0)]
        options = self.valFil(number_set, in_row)

        for column_index in range(self.size):
            if state[column_index][column] != 0:
                in_column.append(state[column_index][column])
        options = self.valFil(options, in_column)

        row_start = int(row/self.height)*self.height
        column_start = int(column/3)*3
        
        for block_row in range(0, self.height):
            for block_column in range(0,3):
                in_block.append(state[row_start + block_row][column_start + block_column])
        options = self.valFil(options, in_block)

        for number in options:
            yield number, row, column      

    def output(self, state, action):
        play = action[0]
        row = action[1]
        column = action[2]
        new_state = copy.deepcopy(state)
        new_state[row][column] = play
        return new_state

    def isValid(self, state):
        total = sum(range(1, self.size+1))
        for row in range(self.size):
            if (len(state[row]) != self.size) or (sum(state[row]) != total):
                return False
            column_total = 0
            for column in range(self.size):
                column_total += state[column][row]
            if (column_total != total):
                return False
        for column in range(0,self.size,3):
            for row in range(0,self.size,self.height):
                block_total = 0
                for block_row in range(0,self.height):
                    for block_column in range(0,3):
                        block_total += state[row + block_row][column + block_column]
                if (block_total != total):
                    return False
        return True

class stateNode:

    def __init__(self, state, action=None):
        self.state = state
        self.action = action

    def expand(self, prob):
        return [self.child_node(prob, action)
                for action in prob.acts(self.state)]

    def child_node(self, prob, action):
        next = prob.output(self.state, action)
        return stateNode(next, action)

def BFS(prob):
    node = stateNode(prob.initial)
    if prob.isValid(node.state):
        return node
    frontier = Queue()
    frontier.put(node)
    while (frontier.qsize() != 0):
        node = frontier.get()
        for child in node.expand(prob):
            if prob.isValid(child.state):
                return child
            frontier.put(child)
    return None

######### run ############

filename = input('Please enter file\'s name (no extention): ')
f = open('testname.txt', 'w')
f.write(filename+'.txt')
f.close()

try:
    xx = n
except:
    import sys
    sys.exit()

start_time = time.time()

prob = Prob(board)
solution = BFS(prob)
elapsed_time = time.time() - start_time

print("Breadth First Search Algorithms")
if solution:
    print ("One solution has been found. Please see the paygame window")
else:
    print ("No solutions")
print ("Time spent: " + str(elapsed_time) + " seconds")

process = psutil.Process(os.getpid())
print('Memory spent: ', process.memory_info().rss, 'bytes')

display(solution.state)
