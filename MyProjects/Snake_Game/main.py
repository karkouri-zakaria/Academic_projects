from random import randrange
from Snake import Snake,Segment,redrawWindow,pygame,COLORS

pygame.init()
WIDTH,ROWS,FPS=400,25,16
WIN = pygame.display.set_mode((WIDTH,WIDTH))

def randomSnack(ROWS, item):
    positions = item.body
    while True:
        x,y = randrange(1,ROWS-1),randrange(1,ROWS-1)
        if len([o for o in positions if o.pos==(x,y)]) > 0 : continue
        break
    return (x,y)

def main():
    run = True
    clock = pygame.time.Clock()
    snake = Snake(COLORS["green"], (10,10))
    snake.addSegment()
    snack = Segment(randomSnack(ROWS,snake), color=COLORS["red"])
    
    while run:
        clock.tick(FPS)
        snake.move()
        headPos = snake.head.pos
        if not (0 <= headPos[0] <= ROWS and 0 <= headPos[1] <= ROWS ):
            snake.reset((10, 10))
        if snake.body[0].pos == snack.pos:
            snake.addSegment()
            snack = Segment(randomSnack(ROWS,snake), color=COLORS["red"])
            
        for x in range(len(snake.body)):
            if snake.body[x].pos in [z.pos for z in snake.body[x+2:]] :
                snake.reset((10,10))
                break
        pygame.display.update()
        redrawWindow(WIN,snake,snack,WIDTH,ROWS)

main()
    

    
