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

def Evaluate(player, state):
    blackscore = CountScores(1, state)
    whitescore = CountScores(2, state)+2.5
    riskblack = 0
    riskwhite = 0
    for i in range(n):
        for j in range(n):
            if state[i][j] == 1:
                liberty = CountLiberty(1, state, i, j)
                if len(liberty) <= 1:
                    riskblack += 1
            elif state[i][j] == 2:
                liberty  = CountLiberty(2, state, i, j)
                if len(liberty) <= 1:
                    riskwhite += 1
    if player == 1:
        approx = blackscore-whitescore-riskblack+riskwhite
    else:
        approx = whitescore-blackscore-riskwhite+riskblack
    return approx

def max_node(player, pre_state, cur_state, alpha, beta, depth):
    if depth == 0:
        value = Evaluate(player, cur_state)
        return value, []

    moves = PossibleMoves(player, pre_state, cur_state)
    if len(moves) == 0:
        return sys.maxsize, "PASS"
    if len(moves) == 25:
        return sys.maxsize, [(2,2)]
    
    localmax = -sys.maxsize
    opt_move = []
    for m in moves:
        new_state = GetNewState(player, pre_state, cur_state, m[0], m[1])
        val, pre_move = min_node(3-player, cur_state, new_state, alpha, beta, depth-1)

        if val > localmax:
            localmax = val
            opt_move = [m]+pre_move
        
        if localmax > beta:
            return localmax, opt_move

        if localmax > alpha:
            alpha = localmax
    return localmax, opt_move

def min_node(player, pre_state, cur_state, alpha, beta, depth):
    if depth == 0:
        value = Evaluate(player, cur_state)
        return value, []

    moves = PossibleMoves(player, pre_state, cur_state)
    if len(moves) == 0:
        return sys.maxsize, "PASS"
    
    localmin = sys.maxsize
    opt_move = []
    for m in moves:
        new_state = GetNewState(player, pre_state, cur_state, m[0], m[1])
        val, action = max_node(3-player, cur_state, new_state, alpha, beta, depth-1)

        if val < localmin:
            localmin = val
            opt_move = [m]+action
        
        if localmin < alpha:
            return localmin, opt_move

        if localmin < beta:
            beta = localmin
    return localmin, opt_move


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
    # count = 0
    liberty = set()
    for p in area:
        neighbors = FindNeighbor(cur_state, p[0], p[1])
        for point in neighbors:
            if cur_state[point[0]][point[1]] == 0:
                # count += 1
                liberty.add(point)
    return list(liberty)

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
    for i in range(n):
        for j in range(n):
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

    # val, result = alphabetapruning(player, player, pre_state, cur_state, -sys.maxsize, sys.maxsize, (), 4)
    val, action = max_node(player, pre_state, cur_state, -sys.maxsize, sys.maxsize, 3)
    if len(action) != 0:
        result = action[0]
    else:
        result = "PASS"
    WriteOutput(result)
    print('total time cost is {}'.format(time.time()-t1))