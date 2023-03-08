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
    def __init__(self, state, player, parent = None, children = None):
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
        self.cur_player = None
        # self.print_myself() ##
    def print_myself(self):
        print('\t Init MCTS:', self, ' root:', self.root)

    def run(self, avail_moves):
        for i in range(100):
            move, node = self.select(self.root, avail_moves) # move is a string formatted as '[x, y]'
            # print('\nroot.children', self.root.children, '\n')
            
            # for n in list(self.root.children.values()):
            #     n.print_myself()
            N, success_num = self.expand(copy.deepcopy(node))
            # print('N, success_num', N, success_num)
            
            # print('child: ', str(move))
            
            # self.root.children[list(self.root.children.keys())[0]].total += N #$$$$$$$$$$
            self.root.children[str(move)].total += N
            self.root.children[str(move)].success += success_num
            print('str(move)', str(move))
            self.root.children[str(move)].print_myself()
            # if '[1, 2]' == str(move):
            #     print('after TES', self.root.children[str(move)].total, self.root.children[str(move)].success)
            # print('EXPAND: N, success_num', N, success_num)
            # self.backpropogate(N, success_num) #################################
        print('my run returns: move', move[1], move[4])
        return [int(move[1]), int(move[4])]

    def select(self, root: Node, avail_moves):
        if root.expanded: 
            for n in list(root.children.values()):
                n.print_myself()
            move, node = self.get_best_node(root.children, self.constant)
        else:
            for m in avail_moves:
                tmp_state = copy.deepcopy(root.state)
                tmp_state[m[0], m[1]] = self.cur_player
                # print('m', m, 'self.cur_player', self.cur_player, 'tmp_state: ', tmp_state)
                root.children[str(m)] = Node(state=tmp_state, player=self.cur_player, parent=root, children=None) ##
                root.children[str(m)].move_str = str(m)
            index = random.randint(0, len(root.children) - 1)
            move = avail_moves[index]
            node = list(root.children.values())[index]
            # print('random', random.randint(0, len(root.children) - 1))
            root.expanded = True
        return str(move), node
    def expand(self, node: Node):
        N = 0
        success_num = 0
        for j in range(100): ###
            tmp_state = copy.deepcopy(node.state)
            cur_player = self.cur_player
            my_score = 0
            oppo_score = 0
            while N < 18: ### loop unitl the termination
                if list(np.array(tmp_state).reshape(1, -1)[0]).count(None) < 1:
                    # print('plot', tmp_state)
                    break
                cur_player = 'X' if cur_player == 'O' else 'O'
                ### available moves
                cur_moves = []
                for x, row in enumerate(tmp_state):
                    for y, cell in enumerate(row):
                        if cell is None and ((x + y) % 2 == 0 and cur_player == 'X' or (x + y) % 2 == 1 and cur_player == 'O'):
                            cur_moves.append([x, y])
                cur_move = random.choice(cur_moves)
                tmp_state[cur_move[0], cur_move[1]] = cur_player
                added_score = self.alignement(tmp_state,cur_move[0], cur_move[1])
                # print('my_score', my_score, 'oppo_score', oppo_score)
                if cur_player == self.cur_player: my_score += added_score
                else: oppo_score += (added_score + 1) #====================================================================================
            # print('========= my_score', my_score, 'oppo_score', oppo_score)
            if my_score >= oppo_score: success_num += 1
            N += 1
        return N, success_num
    def backpropogate(self, N, success_num):
        pass

    def get_best_node(self, children: dict, constant: int): # UCT
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
    
    def get_move(self,state,player):

        # player: 'O' or 'X'

        mem_before = psutil.Process(os.getpid()).memory_info().rss

        # if self.mcts.root == None:
        self.mcts.root = Node(state=state, player=player, parent=None, children={})
        self.mcts.cur_player = player
        self.mcts.time_limit = TIME_LIMIT # sec # haven't applied

        avail_moves = self.available_cells(state,player) # available actions
        avail_moves = [m for m in avail_moves if (m[0] + m[1]) % 2 == 0] if player == 'X' else [m for m in avail_moves if (m[0] + m[1]) % 2 == 1]

        if len(avail_moves) < 100:
            move = self.mcts.run(avail_moves) # This is my turn
            # move = random.choice(avail_moves)
        else:
            move = random.choice(avail_moves)

        mem_after = psutil.Process(os.getpid()).memory_info().rss
        print((mem_after - mem_before) / 1024**2, ' MB')

        return move   
