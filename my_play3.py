"""
CS561 HW2
Game Playing-GO
Alphabeta Pruning
"""
import os
import sys
import time
import math
from random import sample

#global variables for board size and komi
n = 5
komi = n/2
Black = 0
White = 0

def WriteOutput(result):
    f = open("output.txt", "w")
    print(result)
    if result == ("PASS"):
        f.write(result)
    else:
        f.write(str(result[0])+','+str(result[1]))
    f.close()
        
def alphabetapruning(origin, player, pre_state, cur_state, alpha, beta, opt_move, depth):
    # if depth == 0:
        # moves = PossibleMoves(player, pre_state, cur_state)
        # if len(moves) == 0:
        #     return sys.maxsize, ("PASS")
        # # move_score = {}
        # min_val = sys.maxsize
        # for action in moves:
        #     new_state = GetNewState(player, pre_state, cur_state, action[0], action[1])
        #     black = CountScores(2, new_state)
        #     white = CountScores(1, new_state)+komi
        #     if origin == 1:
        #         score = white - black
        #     else:
        #         score = black - white
            
        #     if score < min_val:
        #         min_val = score
        #         min_liberty = CountLiberty(player, new_state, action[0], action[1])
        #         opt = action
        #     elif score == min_val:
        #         liberty = CountLiberty(player, new_state, action[0], action[1])
        #         if liberty < min_liberty:
        #             min_liberty = liberty
        #             min_val = score
        #             opt = action
        # return score, opt
    
    moves = PossibleMoves(player, pre_state, cur_state)
    if len(moves) == 0:
        if player == origin:
            val = alpha
        else:
            val = beta
        return val, ("PASS")
    
    # if len(moves) >= 3:
    #     moves = sample(moves, 3)
    for m in moves:
        new_state = GetNewState(player, pre_state, cur_state, m[0], m[1])
        val, pre_move = alphabetapruning(origin, 3-player, cur_state, new_state, alpha, beta, opt_move, depth-1)
        if player == origin:
            #max node
            if val > alpha:
                alpha = val
                opt_move = tuple(m)
            if val >= beta:
                return val, opt_move
        else:
            #min node
            if val < beta:
                beta = val
                opt_move = tuple(m)
            if val <= alpha:
                return val, opt_move
    if player == origin:
        val = alpha
    else:
        val = beta
    if opt_move == ():
        opt_move = ("PASS")
    return val, opt_move

def PossibleMoves(player, pre_state, cur_state):
    #expand the game tree by finding the possible next move in current state
    valid_move = []
    for i in range(n):
        for j in range(n):
            if cur_state[i][j] == 0 and No_Suicide(player, pre_state, cur_state, i, j):
                valid_move.append((i,j))
    return valid_move

def FindNeighbor(cur_state, row, col):
    neighbors = []
    if row > 0:
        neighbors.append((row-1, col))
    if col > 0:
        neighbors.append((row, col-1))
    if row+1 < n:
        neighbors.append((row+1, col))
    if col+1 < n:
        neighbors.append((row, col+1))
    return neighbors

def OpenLiberty(player, cur_state, row, col):
    #check the liberty of a point
    #first find the area the point can form
    area = []
    s = [(row, col)]
    while s:
        tmp = s.pop()
        area.append(tmp)
        i, j = tmp[0], tmp[1]

        #find the neighbors of the point
        neighbors = FindNeighbor(cur_state, i, j)
        same = []
        for p in neighbors:
            if cur_state[p[0]][p[1]] == cur_state[i][j]:
                same.append(p)

        for x in same:
            if x not in s and x not in area:
                s.append(x)
    #check the liberty of the area
    for p in area:
        neighbors = FindNeighbor(cur_state, p[0], p[1])
        for point in neighbors:
            if cur_state[point[0]][point[1]] == 0:
                return True
    return False

def CountLiberty(player, cur_state, row, col):
    #check the liberty of a point
    #first find the area the point can form
    area = []
    s = [(row, col)]
    while s:
        tmp = s.pop()
        area.append(tmp)
        i, j = tmp[0], tmp[1]

        #find the neighbors of the point
        neighbors = FindNeighbor(cur_state, i, j)
        same = []
        for p in neighbors:
            if cur_state[p[0]][p[1]] == cur_state[i][j]:
                same.append(p)

        for x in same:
            if x not in s and x not in area:
                s.append(x)
    #check the liberty of the area
    count = 0
    for p in area:
        neighbors = FindNeighbor(cur_state, p[0], p[1])
        for point in neighbors:
            if cur_state[point[0]][point[1]] == 0:
                count += 1
    return count

def FindDied(player, cur_state):
    #find the died points in the board if any
    died = []
    for i in range(n):
        for j in range(n):
            if cur_state[i][j] == player and OpenLiberty(player, cur_state, i, j) == False:
                died.append((i, j))
    return died

def RemoveDied(player, cur_state):
    #remove the died points in the board if any
    died = FindDied(player, cur_state)
    if len(died) == 0:
        return cur_state
    else:
        new_state = list(map(list, cur_state))
        for pair in died:
            new_state[pair[0]][pair[1]] = 0
        return new_state

def No_Suicide(player, pre_state, cur_state, i, j):
    #check if it is a suicide move
    #can not place a chess on an existing point
    if cur_state[i][j] != 0:
        return False
    
    #check the Liberty Rule
    new_state = list(map(list, cur_state))
    new_state[i][j] = player
    if OpenLiberty(player, new_state, i, j) == True:
        return True
    
    new_state = RemoveDied(3-player, new_state)
    if OpenLiberty(player, new_state, i, j) == False:
        return False
    #check the KO Rule
    else:
        if new_state == pre_state:
            return False
    return True

def GetNewState(player, pre_state, cur_state, i, j):
    new_state = list(map(list, cur_state))
    # if No_Suicide(player, pre_state, cur_state, i, j):
    new_state[i][j] = player
    new_state = RemoveDied(3-player, new_state)
    return new_state

def CountScores(player, board):
    #find the score in this state
    num = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == player:
                num += 1
    return num

if __name__ == "__main__":
    #begin the clock to calculate the time
    t1 = time.time()

    #read from the input file to get the player and the board state
    f = open("input.txt")
    line = f.readline().strip()
    player = int(line)

    line = f.readline().strip()
    board = []
    while line:
        line = list(map(int, line))
        board.append(line)
        line = f.readline().strip()
    pre_state = board[0:n]
    cur_state = board[n:]

    f.close()

    val, result = alphabetapruning(player, player, pre_state, cur_state, -sys.maxsize, sys.maxsize, (), 4)
    WriteOutput(result)
    print('total time cost is {}'.format(time.time()-t1))
