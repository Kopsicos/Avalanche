import pygame


class Block:
	def __init__(self, colour, grid_xpos, grid_ypos):
		self.colour = colour
		self.grid_xpos = int(grid_xpos)
		self.grid_ypos = int(grid_ypos)
		self.size = 25

	def draw(self, screen):
		pygame.draw.rect(screen, self.colour, [self.grid_xpos*self.size, self.grid_ypos*self.size, self.size-1, self.size-1], 0)
