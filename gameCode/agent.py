import numpy as np
import random
import math

class RandomAgent:
	def __init__(self):
		self.step = 0

	def getAction(self):
		self.step = random.randint(0, 5)
		return 'up down left right bomb stay'.split()[self.step]

	def observe(self, newState, reward, event):
		pass

class ReflexAgent:
	def __init__(self):
		pass

	def getAction(self):
		pass

	def observe(self, newState, reward, event):
		pass

class Agent(object):
	def __init__(self, algorithm):
		if algorithm == "random":
			self.agent = RandomAgent()
		elif algorithm == "reflex":
			self.agent = ReflexAgent()
		
	def get_action(self):
		return self.agent.getAction()

	def observe(self, newState, reward, event):
		self.agent.observe(newState, reward, event)
		