import pygame
from colordict import ColorDict
COLORS=ColorDict()

class Segment():
    def __init__(self, start, dirnx=1, dirny=0, color=COLORS["green"]):
        self.pos,self.dirnx,self.dirny,self.color=start,dirnx,dirny,color

    def move(self, dirnx, dirny):
        self.dirnx,self.dirny = dirnx,dirny
        self.pos  = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
            

    def draw(self, win, width, rows ,eyes=False):
        dis = width // rows
        if self.color==COLORS["red"]:
            pygame.draw.circle(win,self.color,((self.pos[0]+1/2)*dis,(self.pos[1]+1/2)*dis),(dis)//2)
        else:
            pygame.draw.rect(win, self.color, (self.pos[0]*dis+1,self.pos[1]*dis+1,dis-2,dis-2))
        if eyes:
            centre,radius = dis//2,3
            circleMiddle = (self.pos[0]*dis+centre-radius,self.pos[1]*dis+8)
            circleMiddle2 = (self.pos[0]*dis + dis -radius*2, self.pos[1]*dis+8)
            pygame.draw.circle(win, COLORS["black"], circleMiddle, radius)
            pygame.draw.circle(win, COLORS["black"], circleMiddle2, radius)
            pygame.draw.rect(win, COLORS["red"],((self.pos[0]+0.5)*dis,(self.pos[1]+0.75)*dis,dis//12,dis//4))
            pygame.draw.rect(win, COLORS["black"],((self.pos[0]+0.4)*dis,(self.pos[1]+0.75)*dis,dis//5,dis//12))

def redrawWindow(win,snake,snack,width,rows):
    win.fill(COLORS["black"])
    #drawGrid(WIDTH, ROWS, win)
    snake.draw(win,width,rows)
    snack.draw(win,width,rows)
    pygame.display.update()

def drawGrid(WIDTH, ROWS, win):
    x = y = 0
    for l in range(ROWS):
        x+=WIDTH // ROWS
        y+=WIDTH // ROWS
        pygame.draw.line(win, COLORS["white"], (x, 0),(x,WIDTH))
        pygame.draw.line(win, COLORS["white"], (0, y),(WIDTH,y))
    
