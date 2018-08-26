import pygame
import time

# Import GameBoard class
from GameBoard import GameBoard
from GameBoard import GAMEBOARD_HEIGHT

# Import Shape class
from Shape import Shape

from Colours import *

my_font = pygame.font.Font("Soviet2.ttf", 30)


class Level:
	def __init__(self, num_level):
		self.level = num_level
		self.shape = Shape()
		self.next_shape = Shape()
		self.gameboard = GameBoard(WHITE, self.shape.block_list[0].size)
		self.last_time = time.perf_counter()
		self.slow_activation_time = time.perf_counter()
		self.done_level = False
		self.start_time = time.perf_counter()

	def key_check(self):
		if self.event.key == pygame.K_LEFT:
			self.shape.move_left()
		elif self.event.key == pygame.K_RIGHT:
			self.shape.move_right()
		elif self.event.key == pygame.K_SPACE:
			self.gameboard.score += 0.1 - self.shape.block_list[0].grid_ypos * (0.1 / GAMEBOARD_HEIGHT)
			self.shape.drop()
		elif self.event.key == pygame.K_UP:
			self.shape.rotate_clockwise()
		elif self.event.key == pygame.K_DOWN:
			self.shape.rotate_counterclockwise()
		elif self.event.key == pygame.K_t and self.gameboard.num_slow_time > 0:
			self.gameboard.num_slow_time -= 1
			self.gameboard.slow_time_on = True
			self.slow_activation_time = time.perf_counter()
		elif self.event.key == pygame.K_s and self.gameboard.num_swap > 0:
			self.gameboard.num_swap -= 1
			self.gameboard.swap_shape = True

	def update(self):
		# Main event loop
		for self.event in pygame.event.get():
			if self.event.type == pygame.KEYDOWN:
				self.key_check()

		delay = 0.27 - self.level * 0.005
		if self.gameboard.slow_time_on:
			delay *= 2
			if time.perf_counter() - self.slow_activation_time > 6:
				self.gameboard.slow_time_on = False

		if self.gameboard.swap_shape:
			self.shape = self.next_shape
			self.next_shape = Shape()
			self.gameboard.swap_shape = False

		if time.perf_counter() - self.last_time > delay:
			self.last_time = time.perf_counter()
			self.shape.falling()

		if self.shape.active == False:
			self.gameboard.clear_full_rows()
			self.shape = self.next_shape
			self.next_shape = Shape()
		if self.gameboard.check_loss():
			new_score = self.gameboard.score / 2
			num_lines = self.gameboard.num_lines
			self.gameboard = GameBoard(WHITE, self.shape.block_list[0].size)
			self.gameboard.score = new_score
			self.gameboard.num_lines = num_lines
			self.shape = Shape()
			self.next_shape = Shape()
		if time.perf_counter() - self.start_time > 120:
			self.done_level = True

	def draw(self, screen):
		screen.fill(BLACK)
		self.shape.draw(screen)
		self.next_shape.draw_next_shape(screen)
		self.gameboard.draw(screen)
		line_text = my_font.render("Lines: {}".format(self.gameboard.num_lines), 1, WHITE)
		screen.blit(line_text, (325, 270))
		score_text = my_font.render("Pay: {:.3f}".format(self.gameboard.score), 1, WHITE)
		screen.blit(score_text, (325, 300))
		next_shape_text = my_font.render("Next: ", 1, WHITE)
		screen.blit(next_shape_text, (325, 50))
		pygame.draw.rect(screen, WHITE,
						 [325, 100, 6 * self.shape.block_list[0].size, 6 * self.shape.block_list[0].size], 1)
		power_up_text = my_font.render("Power Ups: ", 1, WHITE)
		screen.blit(power_up_text, (350, 525))

		num_swap_text = my_font.render(" x" + str(self.gameboard.num_swap), 1, WHITE)
		screen.blit(num_swap_text, (735, 525))
		swap_image = pygame.image.load("swap.png")
		screen.blit(swap_image, (675, 515))

		num_slow_time_text = my_font.render(" x" + str(self.gameboard.num_slow_time), 1, WHITE)
		screen.blit(num_slow_time_text, (610, 525))
		slow_time_image = pygame.image.load("clock.png")
		screen.blit(slow_time_image, (550, 515))

		level_text = my_font.render("Day: " + str(self.level), 1, WHITE)
		screen.blit(level_text, (325, 325))
