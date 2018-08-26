import pygame
from Colours import *

class CheckBox:
	def __init__(self, xpos, ypos):
		self.xpos = xpos
		self.ypos = ypos
		self.width = 25
		self.height = 25
		self.activated = False

	def click(self, money):
		x, y = pygame.mouse.get_pos()
		if self.xpos < x < (self.xpos + self.width) and self.ypos < y < (self.ypos + self.height):
			if self.activated:
				self.activated = False
				return money + 2
			elif not self.activated and money >= 2:
				self.activated = True
				return money - 2
		return money

	def draw(self, screen):
		pygame.draw.rect(screen, TURQUOISE, [self.xpos, self.ypos, self.width, self.height], 2)
		if self.activated:
			pygame.draw.line(screen, TURQUOISE, (self.xpos, self.ypos), (self.xpos + self.width, self.ypos + self.height), 2)
			pygame.draw.line(screen, TURQUOISE, (self.xpos, self.ypos + self.height), (self.xpos + self.width, self.ypos), 2)