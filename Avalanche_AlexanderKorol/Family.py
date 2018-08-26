from Colours import *

class Family:
	def __init__(self, name, strength):
		self.name = name
		self.strength = strength
		self.sick = False
		self.dead = False
		self.days_hungry = 0
		self.days_sick = 0
		self.days_cold = 0

	def heal(self):
		if self.sick:
			self.sick = False
			self.days_hungry = 0
			self.days_sick = 0
			self.days_cold = 0

	def go_hungry(self):
		if not self.dead:
			self.days_hungry += 1
			if self.days_hungry >= self.strength:
				self.sick = True

	def go_cold(self):
		if not self.dead:
			self.days_cold += 1
			if self.days_cold >= self.strength:
				self.sick = True

	def die(self):
		if self.sick:
			self.days_sick += 1
			if self.days_sick >= self.strength:
				self.heal()
				self.dead = True

	def get_state(self):
		if self.dead:
			return ("DEAD!", CRIMSON)
		healthy = True
		ailments = []
		if self.days_hungry >= self.strength:
			healthy = False
			ailments.append("Hungry")
		if self.days_cold >= self.strength:
			healthy = False
			ailments.append("Cold")
		if self.sick >= self.strength:
			healthy = False
			ailments.append("Sick")

		if healthy:
			return ("Healthy", TURQUOISE)
		else:
			return (" ".join(ailments), YELLOW)