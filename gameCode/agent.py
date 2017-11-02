import numpy as np
import random
import math

class RandomAgent:
	def __init__(self):
		self.step = 0

	def getAction(self):
		'''samples actions in a round-robin manner'''
		self.step = (self.step + 1) % 6
		return 'up down left right bomb stay'.split()[self.step]

	def observe(self, newState, reward, event):
		pass

class Agent(object):
	"""docstring for Agent"""
	def __init__(self, algorithm):
		if algorithm == "random":
			self.agent = RandomAgent()
		
	def get_action(self):
		return self.agent.getAction()

	def observe(self, newState, reward, event):
		self.agent.observe(newState, reward, event)
		