import pygame
from colordict import ColorDict
COLORS=ColorDict()

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.width = width
		self.total_rows = total_rows
		
		self.x = row * width
		self.y = col * width
		self.color = COLORS["black"]
		self.neighbors = []

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == COLORS["red"]

	def is_open(self):
		return self.color == COLORS["green"]

	def is_barrier(self):
		return self.color == COLORS["white"]

	def is_start(self):
		return self.color == COLORS["cyan"]

	def is_end(self):
		return self.color == COLORS["yellow"]

	def reset(self):
		self.color = COLORS["black"]

	def make_start(self):
		self.color = COLORS["cyan"]

	def make_closed(self):
		self.color = COLORS["red"]

	def make_open(self):
		self.color = COLORS["green"]

	def make_barrier(self):
		self.color = COLORS["white"]

	def make_end(self):
		self.color = COLORS["yellow"]

	def make_path(self):
		self.color = COLORS["purple"]

	def draw(self, win):
		pygame.draw.circle(win,self.color,(self.x+self.width/2,self.y+self.width/2),self.width*0.5)
		

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])
		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])
		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])
		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False