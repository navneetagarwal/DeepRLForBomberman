from collections import deque
import random, sys, math, copy
import observableState
import config

class RandomAgent:
	def __init__(self):
		self.step = 0

	def getAction(self):
		self.step = random.randint(0, 5)
		return 'up down left right bomb stay'.split()[self.step]

	def observe(self, newState, reward, event):
		pass

class ReflexAgent:
	def __init__(self):
		self.state = None
		self.config = config.Config()

	def canMove(self, position, board, direction):
		y = position[1]/self.config.TILE_SIZE
		x = position[0]/self.config.TILE_SIZE
		# print ("Curr Pos -> ", (y,x))
		# print (board[x-1][y].type, board[x+1][y].type, board[x][y-1].type, board[x][y+1].type)

		if direction == "left":
			# print (board[x-1][y].type)
			if board[x-1][y].type != self.config.WALL and board[x-1][y].type != self.config.BRICK:
				return 1
			else:
				return 0
		elif direction == "right":
			# print (board[x+1][y].type)
			if board[x+1][y].type != self.config.WALL and board[x+1][y].type != self.config.BRICK:
				return 1
			else:
				return 0
		elif direction == "up":
			# print (board[x][y-1].type)
			if board[x][y-1].type != self.config.WALL and board[x][y-1].type != self.config.BRICK:
				return 1
			else:
				return 0
		elif direction == "down":
			# print (board[x][y+1].type)
			if board[x][y+1].type != self.config.WALL and board[x][y+1].type != self.config.BRICK:
				return 1
			else:
				return 0
		else:
			# Incorrect direction
			return 0

	def getAction(self):

		if self.state != None:
			bombs = self.state.bombs
			userPosition = self.state.userPosition
			enemies = self.state.enemies
			board = self.state.board.board

			# User position
			x = userPosition[1]/self.config.TILE_SIZE
			y = userPosition[0]/self.config.TILE_SIZE

			# Escape from bomb
			for bomb in bombs:
				bombPos = bomb.position
				# print (userPosition[0], userPosition[1])
				# print (bombPos[0], bombPos[1])				
				if bombPos[0] == userPosition[0]:	# Same x-coordinate -> Move left or right
					if self.canMove(userPosition, board, "left"):
						return "left"
					elif self.canMove(userPosition, board, "right"):
						return "right"
				if bombPos[1] == userPosition[1]:	# Same y-coordinate -> Move up or down
					if self.canMove(userPosition, board, "up"):
						return "up"
					elif self.canMove(userPosition, board, "down"):
						return "down"

			# If near brick, then place bomb
			if (board[x][y-1].type == self.config.BRICK or board[x][y+1].type == self.config.BRICK or board[x-1][y].type == self.config.BRICK or board[x+1][y].type == self.config.BRICK):
				# print (x,y)
				# print (board[x][y-1].type, board[x][y+1].type, board[x-1][y].type, board[x+1][y].type)
				return "bomb"
			else:
				return 'up down left right stay'.split()[random.randint(0,4)]

		return 'up down left right bomb stay'.split()[random.randint(0,5)]

	def observe(self, newState, reward, event):
		self.state = newState

class Agent(object):
	def __init__(self, algorithm):
		if algorithm == "random":
			self.agent = RandomAgent()
		elif algorithm == "reflex":
			self.agent = ReflexAgent()
		self.config = config.Config()

	def get_children_start(self, parent, y_length, x_length):
		x = parent[0]
		y = parent[1]
		children = []
		if(x + 40 <= x_length*40):
			children.append((x + 40, y, "right"))
		if(x - 40 >= 40):
			children.append((x - 40, y, "left"))
		if(y + 40 <= y_length * 40):
			children.append((x, y + 40, "down"))
		if(y - 40 >= 40):
			children.append((x, y - 40, "up"))
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
		positions_bombs = [position.position for position in bombs]
		positions_bombs = [(position[0], position[1]) for position in positions_bombs]
		positions_enemies = [position.position for position in enemies]
		positions_enemies = [(position[0], position[1]) for position in positions_enemies]
		# Visited Set
		explored = []
		queue = deque()
		queue.append(((userPosition[0], userPosition[1]), 0, "NONE"))
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
		return -1, "NONE"

	def shortest_distance_adversary(self, userPosition, board, adversary, bombs, enemies):
		H = board.height
		W = board.width
		board = board.board
		explored = []
		positions = [position.position for position in adversary]
		positions = [(position[0], position[1]) for position in positions]
		positions_bombs = [position.position for position in bombs]
		positions_bombs = [(position[0], position[1]) for position in positions_bombs]
		positions_enemies = [position.position for position in enemies]
		positions_enemies = [(position[0], position[1]) for position in positions_enemies]
		queue = deque()
		# Position Tuple, Depth, Direction
		queue.append(((userPosition[0], userPosition[1]), 0, "NONE"))
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
		return -1, "NONE"

	def degree(self, userPosition, board, bombs, enemies, direction, depth):
		print userPosition[0], userPosition[1]
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
		positions_bombs = [position.position for position in bombs]
		positions_bombs = [(position[0], position[1]) for position in positions_bombs]
		positions_enemies = [position.position for position in enemies]
		positions_enemies = [(position[0], position[1]) for position in positions_enemies]
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
				if child not in vector and child not in positions_bombs and child not in positions_enemies and board1[child[1]/self.config.TILE_SIZE][child[0]/self.config.TILE_SIZE].type == self.config.GROUND:
					ans += dfs(child, vector, depth-1)
			vector.pop()
			if ans > 0:
				return 1
			else:
				return 0

		nPoint = userPosition.move((point[0], point[1]))
		t = board.getTile(nPoint)
		if not t.canBombPass():
			return 0
		nPoint = (nPoint[0], nPoint[1])
		explored.append((userPosition[0], userPosition[1]))
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



	def extract_features(self, state):
		# Get distance to nearest brick
		distance_from_brick, direction_from_brick = self.shortest_distance(state.userPosition, self.config.BRICK, state.board, state.bombs, state.enemies)
		# Get distance to nearest powerup_bomb
		distance_from_bomb_up, direction_from_bomb_up = self.shortest_distance(state.userPosition, self.config.BOMB_UP, state.board, state.bombs, state.enemies)
		# Get distance to nearest power_up
		distance_from_power_up, direction_from_power_up = self.shortest_distance(state.userPosition, self.config.POWER_UP, state.board, state.bombs, state.enemies)
		# Get distance to nearest enemy
		distance_from_enemy, direction_from_enemy = self.shortest_distance_adversary(state.userPosition, state.board, state.enemies, state.bombs, state.enemies)
		# Get distance to nearest bomb
		distance_from_bomb, direction_from_bomb = self.shortest_distance_adversary(state.userPosition, state.board, state.bombs, state.bombs, state.enemies)
		# If the bomberman is in range of a bomb
		in_danger = self.in_range(state.userPosition, state.board, state.bombs)
		# Check for degree of freedom i.e. if a n length path exists from here
		degree_of_freedom = self.degree(state.userPosition, state.board, state.bombs, state.enemies, "up", 3)



		print distance_from_brick, direction_from_brick, in_danger, degree_of_freedom


	def get_action(self):
		return self.agent.getAction()

	def observe(self, newState, reward, event):
		self.agent.observe(newState, reward, event)