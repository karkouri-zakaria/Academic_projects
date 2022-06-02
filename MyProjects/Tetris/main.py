import pygame
from colordict import ColorDict
pygame.init()
WIDTH,HEIGHT,ROWS,COLS,FPS = 200,400,12,7,60
ROW,COL=HEIGHT/(ROWS-1),WIDTH/(COLS)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

class Square:
    def __init__(self,i,j,color=ColorDict()["black"]):
        self.i,self.j,self.color=i,j,color
        self.empty=True
    
    def draw(self):
        if not self.empty:
            pygame.draw.rect(WIN,self.color,(self.j*COL,HEIGHT-self.i*ROW,COL,ROW))
    
def make_grid():
        return( [ [ Square(i,j) for i in range(ROWS) ] for j in range(COLS) ] )

def draw_grid(grid):
    for column in grid:
        for square in column:
            square.draw()
    pygame.display.update()

def Free_Col(grid,piece_length,C):
    for j in range(COLS-piece_length,COLS):
        if grid[C][j].empty:
            return False
    return True

def descente(grid,x,y,piece_length):
    for pos in range(y,y+piece_length):
        grid[x][pos-1].empty,grid[x][pos].empty=False,True
        grid[x][pos-1].color=grid[x][pos].color
        grid[x][pos].color=ColorDict()["black"]

def move(grid,x,y,piece_length,direction):
    for pos in range(y,y+piece_length):  
        if x+direction==COLS or x+direction==-1 or  grid[x+direction][pos].empty==False:
            return
    for pos in range(y,y+piece_length):
        grid[x+direction][pos].color=grid[x][pos].color
        grid[x+direction][pos].empty,grid[x][pos].empty=False,True

def rearrange(grid,x,y,piece_length):
    p=grid[x][y].color
    for pos in range(y,y+piece_length-1):
        grid[x][pos].color=grid[x][pos+1].color
    grid[x][y+piece_length-1].color=p

def descenteRapide(grid,x,y,piece_length):
    n=0
    for j in range(y-1,0,-1):
        if grid[x][j].empty :n+=1
        else:break
    if n!=0:
        for pos in range(0,piece_length):
            grid[x][y-n+pos].color=grid[x][y+pos].color
            grid[x][y-n+pos].empty,grid[x][y+pos].empty=False,True

def detecteAlignement(rangee):
    n,x,score,count=len(rangee),rangee[0].color,0,1
    marking=[False for j in range(n)]
    for i in range(1,n):
        y=rangee[i].color
        if y==x and not y.empty: count+=1
        else:
            if count>2:
                score+=count-2
                for j in range(count):marking[i-1-j]=True
            count,x=1,y
    if count>2:
        score+=count-2
        for j in range(count):marking[n-1-j]=True
    return (marking, score)

def scoreRangee(grid,g,i,j,dx,dy):
    if dx==0 and dy==0: return 0
    else:
        x,y,rangee=i,j,[]
        while 0 <=x <COLS and 0<=y<ROWS:
            rangee.append(grid[x][y].color)
            x,y=x+dx,y+dy
        marking,score=detecteAlignement(rangee)
        for p in range(len(rangee)):
            if marking[p]:
                g[i+p*dx][j+p*dy].empty=True
        return score

def clean(grid):
    g=grid.copy()
    score,dx,dy=0,1,1
    for i in range(COLS):
        score+= scoreRangee(grid,g,i,0,dx,dy)
    for j in range(1,ROWS):
        score+= scoreRangee(grid,g,0,j,dx,dy)
    dx,dy=1,0
    for k in range(ROWS):
        score+= scoreRangee(grid,g,0,k,dx,dy)
    dx,dy=1,-1
    for m in range(COLS):
        score+= scoreRangee(grid,g,m,ROWS-1,dx,dy)
    for s in range(ROWS-1):
        score+= scoreRangee(grid,g,0,s,dx,dy)
    dx,dy=0,1
    for r in range(COLS):
        score+= scoreRangee(grid,g,r,0,dx,dy)

def tassementGrille(grid):
    for i in range(COLS):
        p=0
        for j in range(ROWS):
            if grid[i][j].empty()==True:p+=1
            elif p!=0:
                grid[i][j-p],grid[i][j].empty=grid[i][j],True

def create_piece(grid):
        import random as rn
        a=rn.randint(1,2)
        b=rn.randint(0,COLS-1)
        #if Free_Col(grid,COLS,a,b):
        for i in range(a):
            grid[b][ROWS-i-1].color,grid[b][ROWS-i-1].empty=ColorDict()[rn.choice(["red","green","blue"])],False
        return(a,b)

def main(run = True):
    clock = pygame.time.Clock()
    grid=make_grid()
    draw_grid(grid)
    while run:
        clock.tick(FPS)
        a,b=create_piece(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        while ROWS-a-1!=0 and grid[b][ROWS-a-1].empty:
            print(b, ROWS-a)
            pygame.time.delay(500)
            descente(grid,b,ROWS-a,a)
            draw_grid(grid)
            a+=1

    pygame.quit()
if __name__=="__main__":
	main()