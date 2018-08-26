import random
# Import Block class
from Block import Block
# import width
from GameBoard import GAMEBOARD_WIDTH
# import height
from GameBoard import GAMEBOARD_HEIGHT
from GameBoard import active_board_colour
from GameBoard import active_board_spot
from Colours import *
import pygame


# Define the shapes
Z_SHAPE=[[GAMEBOARD_WIDTH//2-1,0], [GAMEBOARD_WIDTH//2-2,0], [GAMEBOARD_WIDTH//2-1,1], [GAMEBOARD_WIDTH//2,1]]
LONG_SHAPE = [[GAMEBOARD_WIDTH//2-1,0], [GAMEBOARD_WIDTH//2-2,0], [GAMEBOARD_WIDTH//2+1,0], [GAMEBOARD_WIDTH//2,0]]
SQUARE_SHAPE = [[GAMEBOARD_WIDTH//2-1,0], [GAMEBOARD_WIDTH//2,1], [GAMEBOARD_WIDTH//2-1,1], [GAMEBOARD_WIDTH//2,0]]
S_SHAPE = [[GAMEBOARD_WIDTH//2-1,0], [GAMEBOARD_WIDTH//2-2,1], [GAMEBOARD_WIDTH//2-1,1], [GAMEBOARD_WIDTH//2,0]]
L_SHAPE = [[GAMEBOARD_WIDTH//2-1,1], [GAMEBOARD_WIDTH//2-1,0], [GAMEBOARD_WIDTH//2-1,2], [GAMEBOARD_WIDTH//2,2]]
ML_SHAPE = [[GAMEBOARD_WIDTH//2,1], [GAMEBOARD_WIDTH//2,0], [GAMEBOARD_WIDTH//2,2], [GAMEBOARD_WIDTH//2-1,2]]
MISTER_T_SHAPE = [[GAMEBOARD_WIDTH//2-1,1], [GAMEBOARD_WIDTH//2-1,0], [GAMEBOARD_WIDTH//2,0], [GAMEBOARD_WIDTH//2-2,0]]
ALL_SHAPES=[Z_SHAPE, LONG_SHAPE, SQUARE_SHAPE, S_SHAPE, L_SHAPE, ML_SHAPE, MISTER_T_SHAPE]
SHAPE_COLOURS = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, MAGENTA]


class Shape:
	def __init__(self):
		self.num_blocks = 4
		randomNum = random.randrange(7)
		self.colour = SHAPE_COLOURS[randomNum]
		self.shape = ALL_SHAPES[randomNum]
		self.block_list = []
		self.active = True
		for i in range(self.num_blocks):
			self.block_list.append(Block(self.colour, self.shape[i][0], self.shape[i][1]))

	def draw(self, screen):
		for b in self.block_list:
			b.draw(screen)

	# Move the shape left
	def move_left(self):
		for b in self.block_list:
			if b.grid_xpos == 0 or active_board_spot[b.grid_xpos -1][b.grid_ypos]:
				return

		for b in self.block_list:
			b.grid_xpos -= 1

	# Move the shape right
	def move_right(self):
		for b in self.block_list:
			if b.grid_xpos == GAMEBOARD_WIDTH -1 or active_board_spot[b.grid_xpos +1][b.grid_ypos]:
				return

		for b in self.block_list:
			b.grid_xpos += 1

	# Move the shape down
	def move_down(self):
		for b in self.block_list:
			if b.grid_ypos == GAMEBOARD_HEIGHT - 1 or active_board_spot[b.grid_xpos][b.grid_ypos+1 ]:
				return

		for b in self.block_list:
			b.grid_ypos += 1

	# Rotate the Shape clockwise
	def rotate_clockwise(self):
		if self.shape != SQUARE_SHAPE:
			new_block_x=[0]*self.num_blocks
			new_block_y=[0]*self.num_blocks
			can_rotate = True

			for i in range(self.num_blocks):
				new_block_x[i] = -(self.block_list[i].grid_ypos - self.block_list[0].grid_ypos) + self.block_list[0].grid_xpos
				new_block_y[i] = (self.block_list[i].grid_xpos - self.block_list[0].grid_xpos) + self.block_list[0].grid_ypos

				if new_block_x[i] < 0 or new_block_x[i] >= GAMEBOARD_WIDTH:
					can_rotate = False
				elif new_block_y[i] < 0 or new_block_y[i] >= GAMEBOARD_HEIGHT:
					can_rotate = False
				elif active_board_spot[new_block_x[i]][new_block_y[i]]:
					can_rotate = False

			if can_rotate:
				for i in range(self.num_blocks):
					self.block_list[i].grid_xpos = new_block_x[i]
					self.block_list[i].grid_ypos = new_block_y[i]

	# Rotate the Shape counterclockwise
	def rotate_counterclockwise(self):
		if self.shape != SQUARE_SHAPE:
			new_block_x=[0]*self.num_blocks
			new_block_y=[0]*self.num_blocks
			can_rotate = True

			for i in range(self.num_blocks):
				new_block_x[i] = (self.block_list[i].grid_ypos - self.block_list[0].grid_ypos) + self.block_list[0].grid_xpos
				new_block_y[i] = -(self.block_list[i].grid_xpos - self.block_list[0].grid_xpos) + self.block_list[0].grid_ypos

				if new_block_x[i] < 0 or new_block_x[i] >= GAMEBOARD_WIDTH:
					can_rotate = False
				elif new_block_y[i] < 0 or new_block_y[i] >= GAMEBOARD_HEIGHT:
					can_rotate = False
				elif active_board_spot[new_block_x[i]][new_block_y[i]]:
					can_rotate = False

			if can_rotate:
				for i in range(self.num_blocks):
					self.block_list[i].grid_xpos = new_block_x[i]
					self.block_list[i].grid_ypos = new_block_y[i]

	# Move the Shape down
	def falling(self):
		for b in self.block_list:
			if b.grid_ypos == GAMEBOARD_HEIGHT - 1 or active_board_spot[b.grid_xpos][b.grid_ypos + 1]:
				self.hit_bottom()

		if self.active:
			for b in self.block_list:
				b.grid_ypos += 1

	def hit_bottom(self):
		self.active = False
		for b in self.block_list:
			active_board_spot[b.grid_xpos][b.grid_ypos] = True
			active_board_colour[b.grid_xpos][b.grid_ypos] = b.colour

	def drop(self):
		while self.active:
			for b in self.block_list:
				if b.grid_ypos == GAMEBOARD_HEIGHT-1 or active_board_spot[b.grid_xpos][b.grid_ypos+ 1]:
					self.hit_bottom()
			if self.active:
				for b in self.block_list:
					b.grid_ypos += 1

	def draw_next_shape(self, screen):
		for b in self.block_list:
			pygame.draw.rect(screen, b.colour, [b.grid_xpos * b.size + 250, b.grid_ypos* b.size + 150, b.size - 1, b.size -1], 0)
