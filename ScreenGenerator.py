import pygame
from constants import *

class ScreenGenerator():
	def __init__(self, space):
		self.space = space
		self.molmap = space.get_map()
		self.size = self.molmap.get_size()
		self.screen = pygame.Surface(SCREEN_SIZE)

	def update(self):
		self.screen.fill((255, 255, 255))

		for m in self.space.get_all_moleculas():
			pygame.draw.circle(self.screen, (0, 0, 0), self.trans_coords(m.get_coords()), 5)
		
		return self.screen

	def trans_coords(self, coords):
		k = SCREEN_SIZE[0] / self.molmap.size[0] 
		return [k * coord for coord in coords]
