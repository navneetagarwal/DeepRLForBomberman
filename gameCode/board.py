import sys, tile, pygame, config

class Board:
	def __init__(self, stage, level, isGraphics):
		file = open("resources/levels/level_" + str(stage) + "-" + str(level) + ".txt","r").readlines()
		self.isGraphics = isGraphics
		self.board = []
		row = 0
		for line in file:
			self.board.append([])
			for col in range(0,len(line)-1):
				# sys.stdout.write(line[col])
				self.board[row].append(tile.Tile(int(line[col]),self.isGraphics))
			# sys.stdout.write("\n")
			row += 1
			# print ""

		self.height = row
		self.width = len(line)

	def getTile(self,point):
		c = config.Config()
		# print "--"
		# print point
		# print "--"
		col = int(point[0]/c.TILE_SIZE)
		row = int(point[1]/c.TILE_SIZE)
		return self.board[row][col]

	def printBoard(self):
		for row in range(self.height):
			rowStr = ""
			for col in range(self.width-1):
				rowStr += str(self.board[row][col].type) + " "
			print(rowStr)
