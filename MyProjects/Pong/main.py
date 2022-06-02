import pygame
from colordict import ColorDict
from Ball import Ball,Ball_Radius
from Paddle import Paddle,PADDLE_DIM
from Movement_and_collisions import handle_collision,handle_paddle_movement
COLORS = ColorDict()

pygame.init()

WIDTH,HEIGHT,FPS=700,500,30

WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pong Game")
SCORE_FONT = pygame.font.SysFont("comicsans", 30)

WINNING_SCORE = 7


def draw(win,paddles,ball,left_score,right_score):
    win.fill(COLORS["black"])

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, COLORS["red"])
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, COLORS["blue"])
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) -right_score_text.get_width()//2, 20))

    for paddle in paddles: paddle.draw(win)

    for i in range(10,HEIGHT,HEIGHT//20):
        if i%2==1: continue
        else : pygame.draw.rect(win,COLORS["white"],(WIDTH//2-2,i,4,HEIGHT//20))

    ball.draw(win)

    pygame.display.update()

def main():
    run=True
    clock=pygame.time.Clock()

    left_score=right_score=0

    left_paddle=Paddle(10 , HEIGHT//2-PADDLE_DIM["PADDLE_HEIGHT"]//2 , PADDLE_DIM["PADDLE_WIDTH"] , PADDLE_DIM["PADDLE_HEIGHT"],COLORS["red"])
    right_paddle=Paddle(WIDTH-10-PADDLE_DIM["PADDLE_WIDTH"] , HEIGHT//2-PADDLE_DIM["PADDLE_HEIGHT"]//2 , PADDLE_DIM["PADDLE_WIDTH"] , PADDLE_DIM["PADDLE_HEIGHT"],COLORS["blue"])

    ball=Ball(WIDTH//2,HEIGHT//2,Ball_Radius)
    while run:
        clock.tick(FPS)
        draw(WIN,[left_paddle,right_paddle],ball,left_score,right_score)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle,right_paddle)

        ball.move()
        handle_collision(ball,left_paddle,right_paddle)

        if keys[pygame.K_SPACE]:
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score=right_score=0

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        won = False
        if left_score >= WINNING_SCORE:
            won,winn_text,winn_color = True,"Left Player Won!",COLORS["red"]
        elif right_score >= WINNING_SCORE:
            won,winn_text,winn_color = True,"Right Player Won!",COLORS["blue"]

        if won:
            text = SCORE_FONT.render(winn_text, 1, winn_color)
            WIN.blit(text, (WIDTH//2 - text.get_width() // 2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(2000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score=right_score=0

    pygame.quit()

if __name__=='__main__':
    main()