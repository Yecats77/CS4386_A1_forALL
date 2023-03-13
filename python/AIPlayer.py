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
import os
import psutil
TIME_LIMIT=10

class Node(object):
    def __init__(self, state, player, parent = None, children = {}):
        self.state = state
        self.player = player
        self.parent = parent
        self.children = children # move: Node
        self.success = 0
        self.total = 0
        self.move_str = None
        self.expanded = False
        # self.print_myself() ##
    def get_state(self):
        return self.state
    def get_player(self):
        return self.player
    def print_myself(self):
        print('\t Init Node: ', self, ' success: ', self.success, ' total: ', self.total, ' move_str ', self.move_str)
    
class MCTS(object):
    def __init__(self):
        self.root = None
        self.time_limit = 0
        self.constant = 1 / np.sqrt(2) ###
        self.player = None
        self.cur_player = None
        # self.print_myself() ##
    def print_myself(self):
        print('\t Init MCTS:', self, ' root:', self.root)

    def run(self, avail_moves):
        for i in range(1000):
            move, node = self.select(self.root, avail_moves) # move is a string formatted as '[x, y]'
            # print('print children twice')
            # for n in list(self.root.children.values()):
            #     print(n.move_str, n.state)
            
            # tmp_avail_moves = list(filter(lambda item: item[0] != int(node.move_str[1]) and item[1] != int(node.move_str[4]), avail_moves))
            # print('tmp_avail_moves', tmp_avail_moves)
            # print('node.move_str', node.move_str)
            # print(node.state)
            self.expand(node) # 这个node还没算成绩
            # print(node.move_str, node.total, node.success)
            # print('N, success_num', N, success_num)
            
            # print('child: ', str(move))
            
            # self.root.children[list(self.root.children.keys())[0]].total += N #$$$$$$$$$$
            # self.root.children[str(move)].total += N
            # self.root.children[str(move)].success += success_num
            # print('str(move)', str(move))
            # self.root.children[str(move)].print_myself()
            # if '[1, 2]' == str(move):
            #     print('after TES', self.root.children[str(move)].total, self.root.children[str(move)].success)
            # print('EXPAND: N, success_num', N, success_num)
            # self.backpropogate(N, success_num) #################################
        keys = list(self.root.children.keys()) # move_str
        values = list(self.root.children.values()) # node
        best_move = str(avail_moves[0])
        best_rate = 0
        for i, child in enumerate(values):
            # print("success rate", child.success / child.total)
            if best_rate < child.success / child.total:
                best_rate = child.success / child.total
                best_move = keys[i]
        return [int(best_move[1]), int(best_move[4])]

    def select(self, root: Node, avail_moves):
        if not root.expanded:
            for m in avail_moves:
                tmp_state = copy.deepcopy(root.state)
                tmp_state[m[0], m[1]] = self.cur_player
                if root.children == None:
                    root.children = {}
                root.children[str(m)] = Node(state=tmp_state, player=self.cur_player, parent=root, children=None) ##
                root.children[str(m)].move_str = str(m)
            root.expanded = True

        move, node = self.get_best_node(root.children, self.constant)            
        return str(move), node
    
    def expand(self, node):
        N = 0
        success_num = 0
        my_score = 0
        oppo_score = 0
        self.cur_player = self.player
        
        # expand top to down
        while True: ###
        # for i in range(6):
            # print('player', self.cur_player)
            self.cur_player = 'X' if self.cur_player == 'O' else 'O'
            if list(np.array(node.state).reshape(1, -1)[0]).count(None) < 1: # termination
                break
            avail_moves = self.available_cells(node.state, self.cur_player)
            avail_moves = self.my_available_cells(avail_moves, self.cur_player)
            move, node = self.select(node, avail_moves)
            score = self.alignement(node.state, int(node.move_str[1]), int(node.move_str[4]))
            # print('avail_moves', avail_moves)
            # print('node', node.move_str)
            # print('node state', node.state)
            # print('score', score)
            if self.cur_player == self.player:
                my_score += score
            else:
                oppo_score += score
        
        # backpropogate down to up
        while True:
            node.total += 1
            if node.player == self.player and my_score > oppo_score or node.player != self.player and my_score < oppo_score: 
                node.success += 1
            if node == self.root:
                break
            node = node.parent

    def backpropogate(self, N, success_num):
        pass

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
        self.mcts = MCTS()

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

        mem_before = psutil.Process(os.getpid()).memory_info().rss

        # if self.mcts.root == None:
        self.mcts.root = Node(state=state, player=player, parent=None, children={})
        self.mcts.cur_player = player
        self.mcts.player = player
        self.mcts.time_limit = TIME_LIMIT # sec # haven't applied

        avail_moves = self.available_cells(state,player) # available actions
        avail_moves = self.my_available_cells(avail_moves, player)

        avail_moves = self.simple_strategy1(avail_moves, state, player)
        if len(avail_moves) == 1:
            return avail_moves[0]

        if len(avail_moves) < 16:
            move = self.mcts.run(avail_moves) # This is my turn
            # move = random.choice(avail_moves)
        else:
            move = random.choice(avail_moves)

        mem_after = psutil.Process(os.getpid()).memory_info().rss
        print((mem_after - mem_before) / 1024**2, ' MB')

        return move   

    def simple_strategy1(self, avail_moves, state, player): 
        # 如果自己三个棋已经有两个棋了，就先不下，避免对方得六分，但是对方可能会得三分
        one_six_line = []
        two_six_line = []
        not_six_line = []
        for move in avail_moves:
            x = move[0]
            y = move[1]
            if list(state[x]).count(player) == 2 and list(state[y]).count(player) == 2:
                two_six_line.append(move)
            elif list(state[x]).count(player) == 2 or list(state[y]).count(player) == 2:
                one_six_line.append(move)
            else:
                not_six_line.append(move)
        # print(player)
        # print(not_six_line)
        # print(one_six_line)
        # print(two_six_line)
        if len(not_six_line) > 0:
            return not_six_line
        elif len(one_six_line) > 0:
            return one_six_line
        else:
            return two_six_line
