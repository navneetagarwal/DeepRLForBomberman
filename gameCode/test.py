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
			children.append((x + 40, y, [0, 1, 0, 0, 0]))
		if(x - 40 >= 40):
			children.append((x - 40, y, [0, 0, 1, 0, 0]))
		if(y + 40 <= y_length * 40):
			children.append((x, y + 40, [0, 0, 0, 1, 0]))
		if(y - 40 >= 40):
			children.append((x, y - 40, [0, 0, 0, 0, 1]))
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
		queue.append(((userPosition[0], userPosition[1]), 0, []))
		explored.append((userPosition[0], userPosition[1]))
		if(board[userPosition[1]/self.config.TILE_SIZE][userPosition[0]/self.config.TILE_SIZE].type == type_req):
			return 0, [1, 0, 0, 0, 0]
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
		return 0, [0, 0, 0, 0, 0]

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
		queue.append(((userPosition[0], userPosition[1]), 0, []))
		# Positions
		explored.append((userPosition[0], userPosition[1]))
		if((userPosition[0], userPosition[1]) in positions):
			return 0, [1, 0, 0, 0, 0]
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
		return 0, [0, 0, 0, 0, 0]

	def degree(self, userPosition, board, bombs, enemies, direction, depth):
		# print userPosition[0], userPosition[1]
		H = board.height
		W = board.width
		board1 = board.board
		point = (0, 0)
		if direction == 'right':
			point = (40,0)
		elif direction == 'left':
			point = (-40,0)
		elif direction == 'up':
			point = (0,-40)
		elif direction == 'down':
			point = (0,40)
		explored = []
		# positions_bombs = [position.position for position in bombs]
		positions_bombs = [(position[0], position[1]) for position in bombs]
		# positions_enemies = [position.position for position in enemies]
		positions_enemies = [(position[0], position[1]) for position in enemies]
		# DFS over all the paths
		def dfs(node, vector, depth):
			if node in vector or node in positions_bombs or node in positions_enemies:
				return 0
			if depth <= 0:
				return 1
			children = self.get_children_start(node, H, W)
			vector.append((node[0], node[1]))
			ans = 0
			for child in children:
				if (child[0], child[1]) not in vector and (child[0], child[1]) not in positions_bombs and (child[0], child[1]) not in positions_enemies and board1[child[1]/self.config.TILE_SIZE][child[0]/self.config.TILE_SIZE].type == self.config.GROUND:
					print child
					ans += dfs(child, vector, depth-1)
			vector.pop()
			if ans > 0:
				return 1
			else:
				return 0

		nPoint = userPosition.move((point[0], point[1]))
		t = board.getTile(nPoint)
		if not t.canBombPass() or (nPoint[0], nPoint[1]) in positions_enemies:
			return 0
		nPoint = (nPoint[0], nPoint[1])
		explored.append((userPosition[0], userPosition[1]))
		print explored
		val = dfs(nPoint, copy.deepcopy(explored), depth-1)
		return val


	def explosiveHelper(self, userPosition, bomb, board, direction):
		if direction == 'right':
			point = (40,0)
		elif direction == 'left':
			point = (-40,0)
		elif direction == 'up':
			point = (0,-40)
		elif direction == 'down':
			point = (0,40)

		x = y = 0
		if (bomb.position == userPosition):
			return 1
		while True:
			x += point[0]
			y += point[1]
			nPoint = bomb.position.move((x,y))
			t = board.getTile(nPoint)
			# hit a block or indestructible object
			if nPoint == userPosition:
				return 1
			if not t.canBombPass():
				return 0
			# check bomb's power, this terminates the recursive loop
			if int(abs(x)/40) == bomb.range or int(abs(y)/40) == bomb.range:
				return 0

	def in_range(self, userPosition, board, explosives):
		ans = 0
		for explosive in explosives:
			ans += self.explosiveHelper(userPosition, explosive, board, 'left')
			ans += self.explosiveHelper(userPosition, explosive, board, 'right')
			ans += self.explosiveHelper(userPosition, explosive, board, 'up')
			ans += self.explosiveHelper(userPosition, explosive, board, 'down')
		if ans > 0:
			return 1
		return 0



if __name__ == "__main__":
	userPosition = pygame.Rect((40,40),(40,40))
	bombs = []
	enemies = []
	bombs.append(pygame.Rect((200,320),(40,40)))
	board = board.Board(1, 1, 0)
	t = Test()
	configure = config.Config()
	# print t.shortest_distance(userPosition, configure.BRICK, board, bombs, enemies)
	print t.degree(userPosition, board, bombs, enemies, "right", 2)
