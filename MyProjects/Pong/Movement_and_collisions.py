from main import COLORS,WIDTH,HEIGHT,pygame

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_z] and left_paddle.y-left_paddle.V>=0 :
        left_paddle.move(True)
    elif keys[pygame.K_s] and left_paddle.y+left_paddle.V+left_paddle.height<=HEIGHT:
        left_paddle.move(False)
    elif keys[pygame.K_UP]and right_paddle.y-right_paddle.V>=0:
        right_paddle.move(True)
    elif keys[pygame.K_DOWN] and right_paddle.y+right_paddle.V+right_paddle.height<=HEIGHT:
        right_paddle.move(False)

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y+ball.radius>=HEIGHT: ball.y_V*=-1
    elif ball.y-ball.radius<=0: ball.y_V *= -1

    if ball.x_V < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_V *= -1

                difference_in_y = (left_paddle.y + left_paddle.height / 2) - ball.y
                red_factor = (left_paddle.height / 2) / ball.Max_V
                y_V = difference_in_y / red_factor
                ball.y_V = -1 * y_V

    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_V *= -1

                difference_in_y = (right_paddle.y + right_paddle.height / 2) - ball.y
                red_factor = (right_paddle.height / 2) / ball.Max_V
                y_V = difference_in_y / red_factor
                ball.y_V = -1 * y_V