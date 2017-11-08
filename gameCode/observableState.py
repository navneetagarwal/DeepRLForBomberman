class ObservableState(object):
	def __init__(self, board, userPosition, enemies, bombs):
		self.board = board
		self.userPosition = userPosition
		self.enemies = enemies
		self.bombs = bombs
				