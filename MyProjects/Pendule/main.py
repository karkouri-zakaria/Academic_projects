import pygame
from math import exp,cos,sin,sqrt,radians
import matplotlib.pyplot as plt

pygame.init()
W,H,FPS=1200,800,60
WIN=pygame.display.set_mode((W,H))
pygame.display.set_caption("Pendule")

Gravity = 9.81
Coeff=.01


class Pendulum: 
    def __init__(self,x,y,length,mass,Theta_0 ,radius=30,time=0, scaling=200):
        self.length, self.mass,self.Theta_0 ,self.time,self.radius =  length*200, mass,radians(Theta_0),time,radius
        self.sp_const=0.2
        self.y0=-(H/3+2*self.length/600)
        self.graph=[[],[],[]]
        self.trajectory=[]
        self.x , self.y = 0 , self.y0

    def update_position(self,dt):
        self.time += dt
        Lambda=Coeff/2*self.mass
        theta1 = self.Theta_0 *exp(-Lambda*self.time)* cos( self.time / sqrt(self.length/Gravity))
        theta2 = exp(-Lambda*self.time)* cos( self.time / sqrt(self.mass/self.sp_const))
        self.x = (self.length - self.y0*cos(theta2))*sin(theta1)
        self.y = (- self.length + self.y0*cos(theta2))*cos(theta1)

    def draw(self):
        WIN.fill((0,0,0))
        pygame.draw.circle(WIN,(255,255,255),(self.x*2+(W/2),(H/3)-self.y),self.radius)
        pygame.draw.circle(WIN,(255,255,255),(W/2,H/3 ),self.radius//4)
        pygame.draw.line(WIN,(255,255,255),(W/2,H/3),(self.x*2+(W/2),(H/3)-self.y))
        self.graph[0].append(self.time)
        self.graph[1].append(self.x)
        self.graph[2].append(self.y)
        self.trajectory.append((self.x*2+(W/2),(H/3)-self.y))
        if pygame.key.get_pressed()[pygame.K_KP_ENTER]:
            pygame.draw.lines(WIN, (255,255,255), False, self.trajectory[2:], 1)
        pygame.display.update()


def pendule(run=True):
    Clock=pygame.time.Clock()
    P=Pendulum(0,0,.2,1,10)
    while run:
        Clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        P.draw()
        P.update_position(.3)


    plt.subplot(2, 1, 1)
    plt.plot(P.graph[0],P.graph[1])
    plt.subplot(2, 1, 2)
    plt.plot(P.graph[0],P.graph[2])
    plt.show()

    pygame.quit()
if __name__=="__main__":
    pendule()