import pygame
import random
from Constants import *
from Colours import WHITE
import math

class Snow:
	def __init__(self):
		self.reset()
		self.ypos = random.randrange(GAME_HEIGHT)

	def draw(self, screen):
		pygame.draw.circle(screen, WHITE, (int(self.xpos), int(self.ypos)), self.size)

	def move(self):
		if self.ypos >= GAME_HEIGHT:
			self.reset()
		else:
			self.timer += random.uniform(-0.1, 0.1)
			self.velocity = math.sin(self.timer)
			self.xpos += self.velocity
			self.ypos += 1

	def reset(self):
		self.xpos = random.randrange(GAME_WIDTH)
		self.ypos = 0
		self.size = random.randint(1, 2)
		self.timer = random.uniform(0, math.pi * 2)
		self.velocity = random.uniform(-1, 1)
