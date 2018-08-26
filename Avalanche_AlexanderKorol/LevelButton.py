import pygame
from Colours import *
from Constants import *
import Global
level_font = pygame.font.Font("Soviet2.ttf", 15)


class LevelButton:
	def __init__(self, num_level, x, y):
		self.level = num_level
		self.size = LEVEL_BUTTON_SIZE
		self.xpos = x
		self.ypos = y
		self.level_text = level_font.render("Day", 1, BLACK)
		self.num_text = level_font.render(str(self.level), 1, BLACK)
		self.level_text_offset = (LEVEL_BUTTON_SIZE - self.level_text.get_width()) // 2
		self.num_text_offset = (LEVEL_BUTTON_SIZE - self.num_text.get_width()) // 2

	def draw(self, screen):
		colour = WHITE if (self.level == Global.max_level or self.level == 1) else GRAY

		pygame.draw.rect(screen, colour, [self.xpos, self.ypos, self.size, self.size], 0)
		screen.blit(self.level_text, (self.xpos + self.level_text_offset,self.ypos + 5))
		screen.blit(self.num_text, (self.xpos + self.num_text_offset, self.ypos + LEVEL_BUTTON_SIZE // 2))

	def is_pressed(self):
		x, y = pygame.mouse.get_pos()
		if self.xpos < x < (self.xpos + LEVEL_BUTTON_SIZE) and self.ypos < y < (self.ypos + LEVEL_BUTTON_SIZE) and (self.level == Global.max_level or self.level == 1):
			return True
		return False
