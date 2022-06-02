from main import COLORS,pygame

Ball_Radius,Ball_speed=7,14



class Ball:
    COLOR,Max_V=COLORS["white"],Ball_speed

    def __init__(self, x, y, radius):
        self.x,self.y,self.radius,self.x_V,self.y_V = self.original_x = x,y,radius,self.Max_V,0
        self.original_x,self.original_y=x,y
    
    def draw(self,win):
        pygame.draw.circle(win,self.COLOR,(self.x,self.y),self.radius)
    def move(self):
        self.x,self.y=self.x+self.x_V,self.y+self.y_V
    
    def reset(self):
        self.x,self.y,self.y_V,self.x_V = self.original_x,self.original_y,0,self.x_V*(-1)