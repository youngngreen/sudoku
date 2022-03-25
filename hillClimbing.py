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

    def isValid(self, state):
        exp_sum = sum(range(1, self.size+1))
        for row in range(self.size):
            if (len(state[row]) != self.size) or (sum(state[row]) != exp_sum):
                return False
            column_sum = 0
            for column in range(self.size):
                column_sum += state[column][row]
            if (column_sum != exp_sum):
                return False

        for column in range(0,self.size,3):
            for row in range(0,self.size,self.height):
                block_sum = 0
                for block_row in range(0,self.height):
                    for block_column in range(0,3):
                        block_sum += state[row + block_row][column + block_column]
                if (block_sum != exp_sum):
                    return False
        return True

    def valFil(self, values, used):
        return [number for number in values if number not in used]

    def getSpt(self, board, state):
        target_option_len = board
        row = 0
        while row < board:
            column = 0
            while column < board:
                if state[row][column] == 0:
                    options = self.rowFil(state, row)
                    options = self.colFil(options, state, column)
                    options = self.quadFil(options, state, row, column)
                    if len(options) < target_option_len:
                        target_option_len = len(options)
                        options = []
                        spotrow = row
                        spotcol = column
                column = column + 1
            row = row + 1                
        return spotrow, spotcol

    def rowFil(self, state, row):
        number_set = range(1, self.size+1)
        in_row = [number for number in state[row] if (number != 0)]
        options = self.valFil(number_set, in_row)
        return options

    def colFil(self, options, state, column):
        in_column = []
        for column_index in range(self.size):
            if state[column_index][column] != 0:
                in_column.append(state[column_index][column])
        options = self.valFil(options, in_column)
        return options

    def quadFil(self, options, state, row, column):
        in_block = []
        row_start = int(row/self.height)*self.height
        column_start = int(column/3)*3
        for block_row in range(0, self.height):
            for block_column in range(0,3):
                in_block.append(state[row_start + block_row][column_start + block_column])
        options = self.valFil(options, in_block)
        return options    

    def acts(self, state):
        row,column = self.getSpt(self.size, state)
        options = self.rowFil(state, row)
        options = self.colFil(options, state, column)
        options = self.quadFil(options, state, row, column)
        for number in options:
            new_state = copy.deepcopy(state)
            new_state[row][column] = number
            yield new_state

class stateNode:
    
    def __init__(self, state):
        self.state = state

    def expand(self, problem):
        return [stateNode(state) for state in problem.acts(self.state)]

def hillClimbing(problem):
    start = stateNode(problem.initial)
    if problem.isValid(start.state):
        return start.state
    stack = []
    stack.append(start)
    while stack: 
        node = stack.pop()
        if problem.isValid(node.state):
            return node.state
        stack.extend(node.expand(problem)) 
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

problem = Prob(board)
solution = hillClimbing(problem)
elapsed_time = time.time() - start_time

print("Hill Climbing Algorithms")
if solution:
    print ("One solution has been found. Please see the paygame window")
else:
    print ("No solutions")

print ("Time spent: " + str(elapsed_time) + " seconds")

process = psutil.Process(os.getpid())
print('Memory spent: ', process.memory_info().rss, 'bytes')

display(solution)