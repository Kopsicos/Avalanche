import pygame
from Colours import *
import random

GAMEBOARD_WIDTH = 12  # how many Blocks wide
GAMEBOARD_HEIGHT = 23  # how many Blocks tall
active_board_spot = [[0 for y in range(GAMEBOARD_HEIGHT)] for x in range(GAMEBOARD_WIDTH)]
active_board_colour = [[0 for y in range(GAMEBOARD_HEIGHT)] for x in range(GAMEBOARD_WIDTH)]

pygame.init()
line_sound = [pygame.mixer.Sound("ZA_WARUDO.wav"), pygame.mixer.Sound("Stop Time.wav"), pygame.mixer.Sound("The Hand noise.wav")]


class GameBoard:
	def __init__(self, colour, block_size):
		self.border_colour = colour
		self.score = 0
		self.num_lines = 0
		self.num_slow_time = 1
		self.num_swap = 1
		self.swap_shape = False
		self.slow_time_on = False
		self.multiplier = block_size
		for c in range(GAMEBOARD_WIDTH):
			for r in range(GAMEBOARD_HEIGHT):
				active_board_spot[c][r] = False
				active_board_colour[c][r] = (0,0,0)

	def draw(self, screen):
		pygame.draw.rect(screen, self.border_colour, [0, 0, GAMEBOARD_WIDTH * self.multiplier, GAMEBOARD_HEIGHT * self.multiplier], 1)
		for c in range(GAMEBOARD_WIDTH):
			for r in range(GAMEBOARD_HEIGHT):
				if active_board_spot[c][r]:
					pygame.draw.rect(screen, active_board_colour[c][r], [c * self.multiplier, r * self.multiplier, self.multiplier - 1, self.multiplier -1], 0)

	def check_loss(self):
		for c in range(GAMEBOARD_WIDTH):
			if active_board_spot[c][0]:
				return True
		return False

	def is_complete_line(self, row_num):
		for c in range(GAMEBOARD_WIDTH):
			if active_board_spot[c][row_num] == False:
				return False
		return True

	def clear_full_rows(self):
		for r in range(GAMEBOARD_HEIGHT):
			if self.is_complete_line(r):
				line_sound[random.randint(0,2)].play()
				self.score += 0.01
				self.num_lines += 1
				for r_above in range(r, 0, -1):
					for c in range(GAMEBOARD_WIDTH):
						active_board_spot[c][r_above] = active_board_spot[c][r_above-1]
						active_board_colour[c][r_above] = active_board_colour[c][r_above - 1]
				for c in range(GAMEBOARD_WIDTH):
					active_board_spot[c][0] = False
					active_board_colour[c][0] = BLACK