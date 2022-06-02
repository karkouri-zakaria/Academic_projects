from Spot import Spot,pygame,COLORS
from Algorithm import algorithm

WIDTH,ROWS = 500,50
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

def make_grid(rows, width):
	return [[Spot(i, j, width // rows, rows) for j in range(rows)] for i in range(rows) ]
	
def draw_grid(win, rows,grid, width):
	for row in grid:
		for spot in row:
			pygame.draw.circle(win,COLORS["lightgrey"],(spot.x+spot.width/2,spot.y+spot.width/2),spot.width/2,int(spot.width/16))

def draw(win, grid, width):
	win.fill(COLORS["black"])
	for row in grid:
		for spot in row:
			if spot.color!=COLORS["black"]:
				spot.draw(win)

	#draw_grid(win, ROWS,grid, width)
	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	y, x = pos
	return y // (width // rows),  x // (width // rows)


def main(win, width,run = True,start = None,end = None):
	grid = make_grid(ROWS, width)
	while run:
		draw(win, grid, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				break

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()
if __name__=="__main__":
	main(WIN, WIDTH)