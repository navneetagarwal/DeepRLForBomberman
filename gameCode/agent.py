import random, sys, math
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
		print ("Curr Pos -> ", (y,x))
		print (board[x-1][y].type, board[x+1][y].type, board[x][y-1].type, board[x][y+1].type)

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
			enemyPositions = self.state.enemyPositions
			board = self.state.board.board

			# User position
			x = userPosition[1]/self.config.TILE_SIZE
			y = userPosition[0]/self.config.TILE_SIZE

			# Escape from bomb
			for bomb in bombs:
				bombPos = bomb.position
				print (userPosition[0], userPosition[1])
				print (bombPos[0], bombPos[1])				
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

	def get_action(self):
		return self.agent.getAction()

	def observe(self, newState, reward, event):
		self.agent.observe(newState, reward, event)
		