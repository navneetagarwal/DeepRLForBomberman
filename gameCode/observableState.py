class ObservableState(object):
	def __init__(self, board, userPosition, enemyPositions, bombPositions):
		self.board = board
		self.userPosition = userPosition
		self.enemyPositions = enemyPositions
		self.bombPositions = bombPositions
				