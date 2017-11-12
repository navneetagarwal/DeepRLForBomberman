import config, pygame, character

class Bomb(pygame.sprite.Sprite):
	fuse = 10
	
	def __init__(self,player,isGraphics):
		self.isGraphics = isGraphics
		pygame.sprite.Sprite.__init__(self)
		self.c = config.Config()
		if self.isGraphics:
			self.image = pygame.image.load(self.c.IMAGE_PATH + "bomb.png").convert()
			self.position = self.image.get_rect()
		else:
			self.position = pygame.Rect((0,0),(40,40))
		self.position = self.position.move((player.position.x,player.position.y))
		self.range = player.power
		self.player = player
		self.triggered = False
	
	def tick(self):
		self.fuse -= 1
		return self.fuse
	
	def explode(self):
		# RFCT - add to player class instead? suggestions?
		self.player.currentBomb += 1
