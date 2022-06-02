from main import COLORS,pygame

PADDLE_DIM={"PADDLE_WIDTH":20,"PADDLE_HEIGHT":100}
Paddle_speed=14

class Paddle:
    COLOR,V=COLORS["white"],Paddle_speed

    def __init__(self,x,y,width,height,color):
        self.x,self.y,self.width,self.height=x,y,width,height
        self.original_x,self.original_y=x,y
        self.COLOR=color
        
    def draw(self,win):
        pygame.draw.rect(win,self.COLOR,(self.x,self.y,self.width,self.height))

    def move(self,up=True):
        self.y=self.y-self.V if up else self.y+self.V
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y