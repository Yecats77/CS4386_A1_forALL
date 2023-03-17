#####################################
# CS4386 Semester B, 2022-2023
# Assignment 1
# Name: LIU Sitong
# Student ID: 56199044
#####################################

import copy 
from math import inf as infinity
import random
import numpy as np
import time
TIME_LIMIT=10

class Node_Stacey(object):
    def __init__(self, state, player, parent = None, children = {}):
        self.state = state
        self.player = player
        self.parent = parent
        self.children = children 
        self.success = 0
        self.total = 0
        self.move_str = None
        self.expanded = False
    def get_state(self):
        return self.state
    def get_player(self):
        return self.player
    
class MCTS_Stacey(object):
    def __init__(self):
        self.root = None
        self.time_limit = 0
        self.constant = 1 / np.sqrt(2) ###
        self.player = None
        self.cur_player = None

    def run(self, state, avail_moves):
        START_TIME = time.time()
        while True:
            if time.time() - START_TIME > self.time_limit - 3:
                break
            move, node = self.select(self.root, avail_moves) # move is a string formatted as '[x, y]'
            self.expand(node) 
        # for c in list(self.root.children.values()):
        #     print('c.success, c.total', c.success, c.total)
        keys = list(self.root.children.keys()) # move_str
        values = list(self.root.children.values()) # node
        best_move = str(avail_moves[0])
        best_rate = 0
        for i, child in enumerate(values):
            if child.total == 0:
                continue
            if best_rate < child.success / child.total:
                best_rate = child.success / child.total
                best_move = keys[i]
        if self.root.children:
            self.root = self.root.children[best_move]
        else:
            self.root = None
            print('================================================')
        return [int(best_move[1]), int(best_move[4])]

    def select(self, root: Node_Stacey, avail_moves):
        if not root.expanded:
            for m in avail_moves:
                tmp_state = copy.deepcopy(root.state)
                tmp_state[m[0], m[1]] = self.cur_player
                if root.children == None:
                    root.children = {}
                root.children[str(m)] = Node_Stacey(state=tmp_state, player=self.cur_player, parent=root, children=None) ##
                root.children[str(m)].move_str = str(m)
            root.expanded = True

        move, node = self.get_best_node(root.children, self.constant)            
        return str(move), node
    
    def expand(self, node):
        my_score = 0
        oppo_score = 0
        self.cur_player = self.player
        
        # expand top to down
        while True: ###
            self.cur_player = 'X' if self.cur_player == 'O' else 'O' # switch player
            if list(np.array(node.state).reshape(1, -1)[0]).count(None) < 1: # termination
                break
            avail_moves = self.available_cells(node.state, self.cur_player)
            avail_moves = self.my_available_cells(avail_moves, self.cur_player)
            move, node = self.select(node, avail_moves)
            score = self.alignement(node.state, int(node.move_str[1]), int(node.move_str[4]))
            if self.cur_player == self.player:
                my_score += score
            else:
                oppo_score += score
        
        # winner has extra 10 points
        if my_score > oppo_score:
            my_score += 10
        elif my_score < oppo_score:
            oppo_score += 10

        # scale the scores
        # my_score *= 0.01
        # oppo_score *= 0.01

        # backpropogate down to up
        while True:
            node.total += my_score + oppo_score
            if node.player == self.player:
                node.success += my_score
            else:
                node.success += oppo_score
            if node == self.root:
                break
            node = node.parent

    def get_best_node(self, children: dict, constant: int): # UCT
        children = self.shuffle_dict(children)
        nodes = list(children.values())
        moves = list(children.keys())
        N = sum([n.total for n in nodes])
        best_u = -np.inf
        best_move = moves[0]
        if N > 0:
            for i in range(len(children)):
                u = nodes[i].success / (nodes[i].total + 1) + constant * np.sqrt(np.log(N) / (nodes[i].total + 1))
                if u > best_u:
                    best_u = u
                    best_move = moves[i]
        return best_move, children[best_move]
    def shuffle_dict(self, d: dict):
        l = list(d.items())
        random.shuffle(l)
        d_shuffled = dict(l)
        return d_shuffled
    
    def alignement(self, grid,x,y):
        score=0
        #1.check horizontal
        if((grid[x][0] != None) and (grid[x][1] != None) and  (grid[x][2]!= None) and (grid[x][3] != None) and (grid[x][4] != None) and (grid[x][5]  != None)): score+=6
        else:
            if (grid[x][0] != None) and (grid[x][1] != None) and  (grid[x][2]!= None) and (grid[x][3] == None):
                if y==0 or y==1 or y==2: score+=3
            elif (grid[x][0] == None) and (grid[x][1] != None) and  (grid[x][2]!= None) and (grid[x][3] != None) and (grid[x][4] == None):
                if y==1 or y==2 or y==3: score+=3
            elif  (grid[x][1] == None) and (grid[x][2] != None) and  (grid[x][3]!= None) and (grid[x][4] != None) and (grid[x][5] == None):
                if y==2 or y==3 or y==4: score+=3
            elif  (grid[x][2] == None) and  (grid[x][3]!= None) and (grid[x][4] != None) and (grid[x][5] != None):
                if y==3 or y==4 or y==5: score+=3
        #2.check vertical
        if((grid[0][y] != None) and (grid[1][y] != None) and (grid[2][y] != None) and (grid[3][y] != None) and (grid[4][y]!= None) and (grid[5][y]!= None)): score+=6
        else:
            if (grid[0][y] != None) and (grid[1][y] != None) and  (grid[2][y]!= None) and (grid[3][y] == None):
                if x==0 or x==1 or x==2: score+=3
            elif (grid[0][y] == None) and (grid[1][y] != None) and  (grid[2][y]!= None) and (grid[3][y] != None) and (grid[4][y] == None):
                if x==1 or x==2 or x==3: score+=3
            elif (grid[1][y] == None) and (grid[2][y] != None) and  (grid[3][y]!= None) and (grid[4][y] != None) and (grid[5][y] == None):
                if x==2 or x==3 or x==4: score+=3
            elif  (grid[2][y] == None) and  (grid[3][y]!= None) and (grid[4][y] != None) and (grid[5][y] != None):
                if x==3 or x==4 or x==5: score+=3
        return score
    def available_cells(self,state,player):
        cells = []
        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if (cell is None):
                    cells.append([x, y])
        return cells
    
    def my_available_cells(self, avail_moves, player):
        return [m for m in avail_moves if (m[0] + m[1]) % 2 == 0] if player == 'X' else [m for m in avail_moves if (m[0] + m[1]) % 2 == 1]


class AIPlayer(object):
    def __init__(self, name, symbole, isAI=False):
        self.name = name
        self.symbole = symbole
        self.isAI = isAI
        self.score=0
        self.mcts = MCTS_Stacey()

    def stat(self):
        return self.name + " won " + str(self.won_games) + " games, " + str(self.draw_games) + " draw."

    def __str__(self):
        return self.name
    def get_isAI(self):
        return self.isAI
    def get_symbole(self):
        return self.symbole
    def get_score(self):
        return self.score
    def add_score(self,score):
    	self.score += score

    def available_cells(self,state,player):
        cells = []
        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if (cell is None):
                    cells.append([x, y])
        return cells
    
    def my_available_cells(self, avail_moves, player):
        return [m for m in avail_moves if (m[0] + m[1]) % 2 == 0] if player == 'X' else [m for m in avail_moves if (m[0] + m[1]) % 2 == 1]
        
    def get_move(self,state,player):

        # player: 'O' or 'X'
        START_TIME = time.time()

        found = False
        if self.mcts.root != None:
            for c in list(self.mcts.root.children.values()):
                if np.array_equal(c.state, state):
                    self.mcts.root = c
                    found = True
                    break
        if not found:
            self.mcts.root = Node_Stacey(state=state, player=player, parent=None, children={})
            self.mcts.cur_player = player
            self.mcts.player = player
            self.mcts.time_limit = TIME_LIMIT # sec # haven't applied

        avail_moves = self.available_cells(state,player) # empty coordinates
        avail_moves = self.my_available_cells(avail_moves, player) # available actions

        if len(avail_moves) == 1:
            return avail_moves[0]

        self.mcts.time_limit -= time.time() - START_TIME
        move = self.mcts.run(state, avail_moves) # This is my turn
        return move   

