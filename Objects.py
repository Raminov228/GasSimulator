from constants import *
import itertools
import copy
import random

class Molecula():
	def __init__(self, coords, velocity, mass=NULL_MASS):
		self.coords = coords
		self.velocity = velocity
		self.mass = mass
		self.momentum = mass * velocity
		self.energy = mass * sum(v**2 for v in velocity) / 2
		self.a = (0, 0)

	def set_coords(self, coords):
		self.coords = coords

	def change_coords(self, dcoords):
		self.coords = [sum(a) for a in zip(self.coords, dcoords)]
		
	def get_coords(self):
		return self.coords

	def set_velocity(self, velocity):
		self.velocity = velocity

	def change_velocity(self, dv):
		self.velocity = [sum(a) for a in zip(self.velocity, dv)]

	def get_velocity(self):
		return self.velocity

	def get_energy(self):
		return self.energy

	def get_clone(self):
		return Molecula(self.coords, self.velocity, self.mass)

	def set_a(self, a):
		self.a = a

	def update(self, dt):
		self.update_coords(dt)		

	def update_coords(self, dt):
		self.change_coords([vx*dt for vx in self.velocity])

	def update_velocity(self, dt):
		self.change_velocity([ax*dt for ax in self.a])		


class Map():
	def __init__(self, moleculas, size=NULL_SIZE, metrics=NULL_METRIX):
		self.moleculas = moleculas
		self.metrics = metrics
		self.amount = len(moleculas)
		self.size = size

	def get_molecula(self, i):
		return self.moleculas[i]

	def get_all_moleculas(self):
		return self.moleculas 

	def transpose(self, dcoords):
		copied_moleculas = [molecula.get_clone() for molecula in self.moleculas]
		for m in copied_moleculas:
			m.change_coords(dcoords)
		return Map(copied_moleculas, self.size, self.metrics)

	def get_size(self):
		return self.size


class Space():
	def __init__(self, molmap):
		self.molmap = molmap
		self.immaps = self.generate_immaps()

	def generate_immaps(self):
		immaps = []
		for trans_koeff in [(0, 1), (0, -1), (1, 1), (1, 0), (1, -1), (-1, -1), (-1, 0), (-1, 1)]:
			immaps.append(self.molmap.transpose([trans_koeff[i] * self.molmap.size[i] for i in range(len(self.molmap.size))]))
		return immaps

	def get_map(self):
		return self.molmap

	def get_immaps(self):
		return self.immaps

	def get_distance(self, m1, m2):
		if m1 == m2:
			return None

		p1_coords = m1.get_coords()
		p2_coords = m2.get_coords()
		r = (sum([(coord[1] - coord[0])**2 for coord in zip(p1_coords, p2_coords)])) ** 0.5
		l = [(coord[1] - coord[0]) / r for coord in zip(p1_coords, p2_coords)]
		return r, l

	def get_all_moleculas(self):
		all_moleculs = self.molmap.get_all_moleculas()[:]
		for immap in self.immaps:
			all_moleculs += immap.get_all_moleculas()[:]
		return all_moleculs

	def get_all_distances(self, m1):
		all_distances = [self.get_distance(m1, m2) for m2 in self.get_all_moleculas()]
		all_distances.remove(None)
		
		return all_distances

	def update(self):
		all_moleculs = []
		for immap in self.immaps:
			all_moleculs += immap.get_all_moleculas()[:]
		
		for m in all_moleculs:
			if 0 <= m.get_coords()[0] <= self.molmap.get_size()[0] and 0 < m.get_coords()[1] < self.molmap.get_size()[1]:
				self.molmap.get_all_moleculas().append(m)

		all_moleculs = self.molmap.get_all_moleculas()
		
		for m in all_moleculs:
			if not (0 <= m.get_coords()[0] <= self.molmap.get_size()[0] and 0 < m.get_coords()[1] < self.molmap.get_size()[1]):
				self.molmap.get_all_moleculas().remove(m)

		self.immaps = self.generate_immaps()


class Gas():
	def __init__(self, size=NULL_SIZE, concentration=NULL_CONCETRATION, mass=NULL_MASS):
		self.concentration = concentration
		self.size = size
		self.molmap = self.generate_random_map()
		self.space = Space(self.molmap)

	#TODO трехмерный случай
	def generate_random_map(self):
		size = self.size
		s = size[0] * size[1]
		self.amount = int(s * self.concentration)
		a = (int(s / self.amount)) ** 0.5
		columns = int(size[0] / a)
		strings = int(size[1] / a)

		moleculas = []

		for j in range(strings):
			for i in range(columns):
				x = i * a + a / 2
				y = j * a + a / 2
				vx = random.random()
				vy = random.random()
				moleculas.append(Molecula((x, y), (vx, vy)))

		return Map(moleculas)

	def get_map(self):
		return self.molmap

	def get_space(self):
		return self.space

	def update(self):
		for m in self.space.get_all_moleculas():
			m.update_coords(TIME_STEP)

		self.update_velocities()

		for m in self.space.get_all_moleculas():
			m.update_velocity(TIME_STEP)

		self.space.update()

	def update_velocities(self):
		for m in self.molmap.get_all_moleculas():
			for r, l in self.space.get_all_distances(m):
				f = self.calc_force(r)
				m.set_a([(f / m.mass) * lx for lx in l])
	
	def calc_force(self, r):
		return EPSILON * ( -(SIGMA / r**13) + (SIGMA / r**7))