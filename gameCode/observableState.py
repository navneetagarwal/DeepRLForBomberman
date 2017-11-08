class ObservableState(object):
	def __init__(self, board, userPosition, enemyPositions, bombs):
		self.board = board
		self.userPosition = userPosition
		self.enemyPositions = enemyPositions
		self.bombs = bombs
				