"""
CS561 HW2
Game Playing
Random, Greedy, Aggressive, Alphabeta Pruning, Q-learning
"""
import os 
import sys
import time
import math
from collections import Counter



if __name__ == "__main__":
    #begin the clock to calculate the time
    #t1 = time.time()
    #read from the input file to get the variables
    n = 5
    f = open("input.txt")
    line = f.readline().strip()
    player = int(line)

    # line = f.readlines()
    line = f.readline().strip()   
    board = []
    while line:
        # tmp = line
        line = list(map(int, line))
        # tmp = list(map(int, tmp))
        board.append(line)
        line = f.readline().strip()
    pre_state = board[0:n]
    cur_state = board[n:]
    print(pre_state)
    print(cur_state)
    f.close()
    #print('total time cost is {}'.format(time.time()-t1))