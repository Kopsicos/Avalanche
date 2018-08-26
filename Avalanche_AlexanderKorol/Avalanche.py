# import the pygame
import pygame
# Import time
import time
from Snow import Snow
from Level import Level
from LevelButton import LevelButton
from Colours import *
from Family import Family
from Constants import *
from CheckBox import CheckBox
import Global
import random

# continue writing the story

def reset():
	Global.max_level = 1
	Global.savings = 10


	Global.family_list = [Family("Brother", 6), Family("Wife", 4), Family("Son", 5), Family("Mother-in-Law", 2),
						  Family("Uncle", 3)]


if __name__ == "__main__":
	try:
		file = open("Save.txt", "r")
		Global.max_level = int(file.readline().rstrip())
		Global.savings = float(file.readline().rstrip())
		Global.family_list = []
		for i in range(0, 5):
			Global.family_list.append(Family(file.readline().rstrip(), int(file.readline().rstrip())))
			Global.family_list[i].sick = file.readline().rstrip() == "True"
			Global.family_list[i].dead = file.readline().rstrip() == "True"
			Global.family_list[i].days_hungry = int(file.readline().rstrip())
			Global.family_list[i].days_sick = int(file.readline().rstrip())
			Global.family_list[i].days_cold = int(file.readline().rstrip())
		file.close()
	except Exception as e:
		print("Failed to Load Save File")
		print(e)
		reset()

	# initialize the game
	pygame.init()

	pygame.mixer.init()
	pygame.mixer.music.load("The Complex.mp3")
	pygame.mixer.music.play(-1)  # Loop song
	type_writer_sound = pygame.mixer.Sound("Typewriter.ogg")
	size = (GAME_WIDTH, GAME_HEIGHT)
	started = False
	title_screen = pygame.image.load("Backdrop.png")
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("Avalanche")

	snow_list = [Snow() for i in range(1337)]

	intro_font = pygame.font.Font("TravelingTypewriter.otf", 15)
	expenses_font = pygame.font.Font("Soviet2.ttf", 30)
	title_font = pygame.font.Font("Soviet2.ttf", 45)
	title_text = title_font.render("Choose Day", 1, WHITE)
	title_text_offset = (GAME_WIDTH - title_text.get_width()) // 2

	level_button_list = []
	button_offset_x = (GAME_WIDTH - (5 * LEVEL_BUTTON_SIZE + 4 * LEVEL_BUTTON_GAP)) // 2
	button_offset_y = GAME_HEIGHT - (6 * LEVEL_BUTTON_SIZE + 4 * LEVEL_BUTTON_GAP)
	for i in range(1, 26):
		level_button_list.append(
			LevelButton(i, button_offset_x + (((i - 1) % 5) * (LEVEL_BUTTON_SIZE + LEVEL_BUTTON_GAP)),
						button_offset_y + (((i - 1) // 5) * (LEVEL_BUTTON_SIZE + LEVEL_BUTTON_GAP))))

while not started:
	screen.blit(title_screen, (0, 0))

	for snow in snow_list:
		snow.move()
		snow.draw(screen)
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			Global.done = True
			started = True
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				started = True


def pick_level():
	chose_level = False
	level = -1
	while not (Global.done or chose_level):
		screen.fill(BLACK)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Global.done = True
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				for b in level_button_list:
					if b.is_pressed():
						level = b.level
						chose_level = True
						break

		screen.blit(title_text, (title_text_offset, 130))
		for b in level_button_list:
			b.draw(screen)
		pygame.display.flip()  # Update screen
	return level


def crop_text(text, letters):
	display_text = []
	displayed_letters = 0
	for line in text:
		if displayed_letters >= letters:
			break
		elif len(line) + displayed_letters <= letters:
			display_text.append(line)
			displayed_letters += len(line)
		elif displayed_letters < letters:
			display_text.append(line[:(letters - displayed_letters)])
			break
	return display_text


def draw_centered_text(text, font=title_font):
	for i in range(0, len(text)):
		line_text = font.render(text[i], 1, WHITE)
		x = (GAME_WIDTH - line_text.get_width()) // 2
		y_offset = (GAME_HEIGHT - len(text) * font.get_linesize()) // 2
		y = y_offset + i * font.get_linesize()
		screen.blit(line_text, (x, y))


def level_intro(level):
	try:
		file_name = "IntroText/Intro{}.txt".format(level)
		file = open(file_name, "r")
		intro_text = file.read()
		file.close()
	except IOError as e:
		intro_text = "Press Enter to Start Day"
	pygame.mixer.music.load(random.choice(["Lightless Dawn.mp3", ("Horizon.mp3"), ("Breath.mp3"), ("The Pit.mp3")]))

	pygame.mixer.music.play(-1)  # Loop song
	try:
		file_name = "PaperText/Paper{}.txt".format(level)
		file = open(file_name, "r")
		paper_text = file.read()
		file.close()
	except IOError as e:
		paper_text = "Press Enter to Start Day"

	intro_lines = intro_text.splitlines()
	continued = False
	last_letter_time = time.perf_counter()
	intro_text_max_letters = 0
	letters = 0
	for line in intro_lines:
		intro_text_max_letters += len(line)
	type_writer_sound.play(-1)
	while not (Global.done or continued):
		screen.fill(BLACK)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Global.done = True
			elif event.type == pygame.KEYDOWN:
				continued = True
		if time.perf_counter() - last_letter_time > 0.125 and letters < intro_text_max_letters:
			letters += 1
			last_letter_time = time.perf_counter()
		if letters >= intro_text_max_letters:
			type_writer_sound.stop()
		draw_centered_text(crop_text(intro_lines, letters), intro_font)
		pygame.display.flip()
	type_writer_sound.stop()

	continued = False
	paper_lines = paper_text.splitlines()
	paper_width = 0
	for s in paper_lines:
		line_width = intro_font.size(s)[0]
		if paper_width < line_width:
			paper_width = line_width
	paper_width += 50
	paper_height = len(paper_lines) * intro_font.get_linesize() + 50
	paper_x = (GAME_WIDTH - paper_width) // 2
	paper_y = (GAME_HEIGHT - paper_height) // 2
	while not (Global.done or continued):
		screen.fill(BLACK)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Global.done = True
			elif event.type == pygame.KEYDOWN:
				continued = True
		pygame.draw.rect(screen, WHITE, [paper_x, paper_y, paper_width, paper_height], 0)
		for i in range(0, len(paper_lines)):
			line_text = intro_font.render(paper_lines[i], 1, BLACK)
			x = paper_x + 25
			y_offset = paper_y + 25
			y = y_offset + i * intro_font.get_linesize()
			screen.blit(line_text, (x, y))
		pygame.display.flip()





def family_screen():
	continued = False
	check_box_list = []
	check_box_list.append(CheckBox(450, 55))
	check_box_list.append(CheckBox(450, 85))
	check_box_list.append(CheckBox(450, 115))
	money = Global.savings + current_level.gameboard.score - 3
	while not (Global.done or continued):

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Global.done = True
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				continued = True
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				for b in check_box_list:
					money = b.click(money)

		screen.fill(BLACK)
		expense_text = expenses_font.render("Manage your expenses using the checkboxes below", 1, WHITE)
		screen.blit(expense_text, (10, 10))
		savings_text = expenses_font.render("Savings {:.3f}".format(Global.savings), 1, WHITE)
		screen.blit(savings_text, (10, 50))
		salary_text = expenses_font.render("Salary {:.3f}".format(current_level.gameboard.score), 1, WHITE)
		screen.blit(salary_text, (10, 80))
		rent_text = expenses_font.render("Rent 3", 1, WHITE)
		screen.blit(rent_text, (10, 110))
		total_text = expenses_font.render("Total {:.3f}".format(money), 1, WHITE)
		screen.blit(total_text, (10, 140))
		food_text = expenses_font.render("Food 2", 1, WHITE)
		screen.blit(food_text, (300, 50))
		heat_text = expenses_font.render("Heat 2", 1, WHITE)
		screen.blit(heat_text, (300, 80))
		medicine_text = expenses_font.render("Medicine 2", 1, WHITE)
		screen.blit(medicine_text, (300, 110))

		for i in range(0, len(Global.family_list)):
			name_text = expenses_font.render(Global.family_list[i].name, 1, WHITE)
			screen.blit(name_text, (10, 300 + i * 30))
			state, state_colour = Global.family_list[i].get_state()
			state_text = expenses_font.render(state, 1, state_colour)
			screen.blit(state_text, (200, 300 + i * 30))
		for b in check_box_list:
			b.draw(screen)
		pygame.display.flip()

	if continued:
		Global.savings = money
		for f in Global.family_list:
			if check_box_list[0].activated:
				f.days_hungry = 0
			else:
				f.go_hungry()
			if check_box_list[0].activated:
				f.days_cold = 0
			else:
				f.go_cold()
			if check_box_list[0].activated:
				f.heal()
			else:
				f.die()


def endings():
	money = Global.savings + current_level.gameboard.score - 2
	ending = False
	dead_family = True
	for f in Global.family_list:
		if not f.dead:
			dead_family = False
			break
	if money < 0:
		ending = True
		end_file = "Endings/Debt Ending.txt"
		pygame.mixer.music.load("Bump in the Night.ogg")
		pygame.mixer.music.play(-1)  # Loop song
	elif dead_family:
		ending = True
		end_file = "Endings/Family Dead Ending.txt"
		pygame.mixer.music.load("Bump in the Night.ogg")
		pygame.mixer.music.play(-1)  # Loop song
	elif Global.max_level > 25:
		ending = True
		end_file = "Endings/Good Job Ending.txt"
		pygame.mixer.music.load("Nowhere Land.ogg")
		pygame.mixer.music.play(-1)  # Loop song
	if ending:
		try:
			file = open(end_file, "r")
			end_text = file.read().splitlines()
			file.close()
		except IOError as e:
			end_text = "ENDING"

		last_letter_time = time.perf_counter()
		letters = 0
		max_letters = 0
		for line in end_text:
			max_letters += len(line)
		type_writer_sound.play(-1)
		while not Global.done:
			screen.fill(BLACK)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					Global.done = True
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
					Global.done = True

			if time.perf_counter() - last_letter_time >= 0.125 and letters < max_letters:
				letters += 1
				last_letter_time = time.perf_counter()
			if letters >= max_letters:
				type_writer_sound.stop()

			draw_centered_text(crop_text(end_text, letters), intro_font)
			pygame.display.flip()
		type_writer_sound.stop()


while not Global.done:
	num_level = pick_level()

	if num_level == 1 and not Global.done:
		reset()
	level_intro(num_level)

	current_level = Level(num_level)
	while not (current_level.done_level or Global.done):
		if pygame.event.peek(pygame.QUIT):
			Global.done = True
		else:
			current_level.update()
			current_level.draw(screen)
			pygame.display.flip()  # Update screen

	finished = False
	while not (Global.done or finished):
		screen.fill(BLACK)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Global.done = True
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				finished = True

		shift_text = []
		shift_text.append("Your Shift has Ended")
		shift_text.append("You have destroyed {} lines of garbage".format(current_level.gameboard.num_lines))
		shift_text.append("Your pay for the day is: {:.3f}".format(current_level.gameboard.score))
		shift_text.append("Press enter to continue")
		draw_centered_text(shift_text)
		pygame.display.flip()  # Update screen

	if current_level.done_level and not Global.done:
		Global.max_level = num_level + 1
		endings()
		family_screen()
		pygame.mixer.music.load("The Complex.mp3")
		pygame.mixer.music.play(-1)  # Loop song




file = open("Save.txt", "w")
lines = []
lines.append(str(Global.max_level))
lines.append(str(Global.savings))
for f in Global.family_list:
	lines.extend(
		[f.name, str(f.strength), str(f.sick), str(f.dead), str(f.days_hungry), str(f.days_sick), str(f.days_cold)])
file.write("\n".join(lines))
file.close()
