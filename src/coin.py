import pygame

class Coin:
	def __init__ (self,x,y):
		self.image = pygame.image.load("images/coin.png").convert_alpha()
		self.rect = self.image.get_rect(center = (x,y))
	def draw(self,screen):
		screen.blit(self.image,self.rect)

