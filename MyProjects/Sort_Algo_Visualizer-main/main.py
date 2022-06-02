import pygame
from random import randint
from colordict import ColorDict
COLORS = ColorDict()

pygame.init()
FPS=120
class DrawInformation:
	BACKGROUND_COLOR = COLORS["white"]
	GRADIENTS = [COLORS["lightgrey"],COLORS["grey"],COLORS["darkgrey"]]
	FONT = pygame.font.SysFont('arial', 30)
	LARGE_FONT = pygame.font.SysFont('arial', 40)
	TOP_PAD = 140

	def __init__(self, width, height, lst):
		self.width,self.height = width,height
		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Sorting Algorithm Visualization")
		self.set_list(lst)

	def set_list(self, lst):
		self.lst,self.min_val,self.max_val = lst,min(lst),max(lst)
		self.block_width = self.width / len(lst)
		self.block_height = ((self.height- self.TOP_PAD) / (self.max_val - self.min_val))

def draw(draw_info, algo_name, ascending):
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)
	title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, COLORS["green"])
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))
	controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, COLORS["black"])
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))
	sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | P - Python Sort | S - Selection Sort", 1, COLORS["black"])
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))
	draw_list(draw_info)
	pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst
	if clear_bg:
		clear_rect = (0, draw_info.TOP_PAD, draw_info.width, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
	for i, val in enumerate(lst):
		x = i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
		color = draw_info.GRADIENTS[i % 3]
		if i in color_positions:
			color = color_positions[i] 
		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
	if clear_bg:
		pygame.display.update()


def generate_starting_list(n, min_val, max_val):
	return [randint(min_val, max_val) for i in range(n)]


def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst
	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]
			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(draw_info, {j: COLORS["green"], j + 1: COLORS["red"]}, True)
				yield True

def selection_sort(draw_info,ascending=True):
	lst = draw_info.lst
	while True:
		for i in range(len(lst)):
			pos = i
			for j in range(i+1, len(lst)):
				if lst[pos] < lst[j] and ascending==False:
					pos = j
				elif lst[pos] > lst[j] and ascending==True:
					pos = j
				draw_list(draw_info,{pos:COLORS["yellow"], j: COLORS["red"],i: COLORS["green"]},True)
			lst[i], lst[pos] = lst[pos], lst[i]
			yield True
		break
	return lst

def python_sort(draw_info, ascending=True):
	draw_info.lst.sort(reverse=not ascending)
	yield True

def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst
	for i in range(1, len(lst)):
		current = lst[i]
		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending
			if not ascending_sort and not descending_sort:
				break
			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(draw_info, {i - 1: COLORS["green"], i: COLORS["red"]}, True)
			yield True
	return lst

def main():
	run = True
	clock = pygame.time.Clock()

	n,min_val,max_val = 100,0,100

	lst = generate_starting_list(n, min_val, max_val)
	draw_info = DrawInformation(1000, 600, lst)
	sorting,ascending = False,True

	sorting_algorithm = python_sort
	sorting_algo_name = "Python Sort"
	sorting_algorithm_generator = None

	while run:
		clock.tick(FPS)
		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = False
		else:
			draw(draw_info, sorting_algo_name, ascending)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type != pygame.KEYDOWN:
				continue
			if event.key == pygame.K_r:
				lst = generate_starting_list(n, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False
			elif event.key == pygame.K_SPACE and sorting == False:
				sorting = True
				sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
			elif event.key == pygame.K_a and not sorting:
				ascending = True
			elif event.key == pygame.K_d and not sorting:
				ascending = False
			elif event.key == pygame.K_i and not sorting:
				sorting_algorithm = insertion_sort
				sorting_algo_name = "Insertion Sort"
			elif event.key == pygame.K_b and not sorting:
				sorting_algorithm = bubble_sort
				sorting_algo_name = "Bubble Sort"
			elif event.key == pygame.K_p and not sorting:
				sorting_algorithm = python_sort
				sorting_algo_name = "Python Sort"
			elif event.key == pygame.K_s and not sorting:
				sorting_algorithm = selection_sort
				sorting_algo_name = "Selection Sort"


	pygame.quit()


if __name__ == "__main__":
	main()