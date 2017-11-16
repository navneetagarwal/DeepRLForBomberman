from collections import deque
import random, sys, math, copy
import observableState, agent, tile
import config, pygame, board
from network import network
import numpy as np



class Test:
	def __init__(self):
		self.config = config.Config()
		pass

	def get_children_start(self, parent, y_length, x_length):
		x = parent[0]
		y = parent[1]
		children = []
		if(x + 40 <= x_length*40):
			children.append((x + 40, y, 0))
		if(x - 40 >= 40):
			children.append((x - 40, y, 1))
		if(y + 40 <= y_length * 40):
			children.append((x, y + 40, 2))
		if(y - 40 >= 40):
			children.append((x, y - 40, 3))
		return children

	def get_children(self, parent, y_length, x_length, direction):
		x = parent[0]
		y = parent[1]

		children = []
		if(x + 40 <= x_length*40):
			children.append((x + 40, y, direction))
		if(x - 40 >= 40):
			children.append((x - 40, y, direction))
		if(y + 40 <= y_length * 40):
			children.append((x, y + 40, direction))
		if(y - 40 >= 40):
			children.append((x, y - 40, direction))
		return children

	def shortest_distance(self, userPosition, type_req, board, bombs, enemies):
		H = board.height
		W = board.width
		board = board.board
		# positions = [position.position for position in adversary]
		positions = [(position[0], position[1]) for position in adversary]
		# positions_bombs = [position.position for position in bombs]
		positions_bombs = [(position[0], position[1]) for position in bombs]
		# positions_enemies = [position.position for position in enemies]
		positions_enemies = [(position[0], position[1]) for position in enemies]
		# Visited Set
		explored = []
		queue = deque()
		queue.append(((userPosition[0], userPosition[1]), 0, -1))
		explored.append((userPosition[0], userPosition[1]))
		start = 1
		while queue:
			node = queue.popleft()
			if start == 1:
				children = self.get_children_start(node[0], H, W)
				start = 2
			else:
				children = self.get_children(node[0], H, W, node[2])
			for child in children:
				if(board[child[1]/self.config.TILE_SIZE][child[0]/self.config.TILE_SIZE].type == type_req):
					return node[1]+1, child[2]
			for child in children:
				if (child[0], child[1]) not in explored and (child[0], child[1]) not in positions_bombs and (child[0], child[1]) not in positions_enemies and board[child[1]/self.config.TILE_SIZE][child[0]/self.config.TILE_SIZE].type == self.config.GROUND:
					queue.append(((child[0], child[1]), node[1]+1, child[2]))
					explored.append((child[0], child[1]))
		return -1, -1


	def shortest_distance_adversary(self, userPosition, board, adversary, bombs, enemies):
		H = board.height
		W = board.width
		board = board.board
		explored = []
		# positions = [position.position for position in adversary]
		positions = [(position[0], position[1]) for position in adversary]
		# positions_bombs = [position.position for position in bombs]
		positions_bombs = [(position[0], position[1]) for position in bombs]
		# positions_enemies = [position.position for position in enemies]
		positions_enemies = [(position[0], position[1]) for position in enemies]
		queue = deque()
		# Position Tuple, Depth, Direction
		queue.append(((userPosition[0], userPosition[1]), 0, -1))
		# Positions
		explored.append((userPosition[0], userPosition[1]))
		start = 1
		while queue:
			node = queue.popleft()
			# If enemy is found
			if start == 1:
				children = self.get_children_start(node[0], H, W)
				start = 2
			else:
				children = self.get_children(node[0], H, W, node[2])
			for child in children:
				if (child[0], child[1]) in positions:
					return node[1]+1, child[2]
			for child in children:
				if (child[0], child[1]) not in explored and (child[0], child[1]) not in positions_bombs and (child[0], child[1]) not in positions_enemies and board[child[1]/self.config.TILE_SIZE][child[0]/self.config.TILE_SIZE].type == self.config.GROUND:
					queue.append(((child[0], child[1]), node[1]+1, child[2]))
					explored.append((child[0], child[1]))
		return -1, -1



if __name__ == "__main__":
	userPosition = pygame.Rect((40,280),(40,40))
	bombs = []
	enemies = []
	bombs.append(pygame.Rect((80,280),(40,40)))
	board = board.Board(1, 1, 0)
	t = Test()
	print board.board[320/40][120/40].type
	configure = config.Config()
	# print t.shortest_distance(userPosition, configure.BRICK, board, bombs, enemies)
	print t.shortest_distance_adversary(userPosition, board, bombs, bombs, enemies)
