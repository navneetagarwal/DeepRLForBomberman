import pygame, config

# RFCT NEEDED
class Character(pygame.sprite.Sprite):
	lives = 1
	speed = 1

	def __init__(self, name, imageName, point, isGraphics):
		self.isGraphics = isGraphics
		pygame.sprite.Sprite.__init__(self)
		self.c = config.Config()
		self.name = name
		self.imageName = imageName
		self.sPosition = point
		if not self.isGraphics:
			self.position = pygame.Rect(point,(40, 40))
		self.reset(True)

	def reset(self,bool):
		if self.isGraphics:
			self.getImage('down')
			self.position = self.image.get_rect()
		else:
			self.position = pygame.Rect((0,0),(40, 40))
		self.move(self.sPosition)

	def getImage(self, direction):
		imagePath = self.c.IMAGE_PATH + self.imageName + direction + ".png"
		self.image = pygame.image.load(imagePath).convert()
		
	def update(self):
		print "=D"

	def movement(self,key):
		c = config.Config()

		if key == pygame.K_UP:
			if self.isGraphics:
				self.getImage('up')
			return [0, -1*c.TILE_SIZE]
		elif key == pygame.K_DOWN:
			if self.isGraphics:
				self.getImage('down')
			return [0, c.TILE_SIZE]
		elif key == pygame.K_LEFT:
			if self.isGraphics:
				self.getImage('left')
			return [-1*c.TILE_SIZE, 0]
		elif key == pygame.K_RIGHT:
			if self.isGraphics:
				self.getImage('right')
			return [c.TILE_SIZE, 0]

	def move(self,point):
		self.old = self.position
		self.position = self.position.move(point)
