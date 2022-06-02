import pygame
from math import cos,sin,sqrt,atan2
from Solar_System import *
from random import randint
from colordict import ColorDict
COLORS = ColorDict()

pygame.init()

WIDTH,HEIGHT,FPS=1000,1000,20
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Planet Simulation")


stars = [[randint(0, WIDTH),randint(0, HEIGHT)] for x in range(200)]
class Planet:
    AU=149597870700
    G=6.67430e-11
    SCALE= 250/AU    # 1AU = 100 pixels
    TIMESTEP=86400  # 1 day
    SIZE=1
    FONT = pygame.font.SysFont("arial", int(SCALE*1e10*7/8))

    def __init__(self,name,x,y,radius,color,mass,initial_velo,rings):
        self.name,self.x,self.y,self.radius,self.color,self.mass,self.x_vel,self.y_vel,self.rings=name,x,y,radius,color,mass,0,initial_velo,rings
        self.sun,self_d_to_sun=False,0
        self.orbit=[]

    def draw(self,win):
        x,y=self.x*self.SCALE+WIDTH/2,self.y*self.SCALE+WIDTH/2
        r=abs(self.radius*self.SCALE*10000 if self.sun==True else self.radius*self.SCALE*10000*Planet.SIZE)
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x,y = x * self.SCALE + WIDTH / 2,y * self.SCALE + HEIGHT / 2 
                updated_points.append((x, y))
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_KP_ENTER]:
                pygame.draw.lines(win, self.color, False, updated_points, 1)

        pygame.draw.circle(win,self.color,(x,y),r)
		
        if not self.sun:
            distance_text = self.FONT.render("R="+f"{round(self.distance_to_sun/self.AU,4)} AU", 1, COLORS["green"])
            win.blit(distance_text, (x-r-25, y-r-25))
        name_text = self.FONT.render(self.name, 1, self.color)
        win.blit(name_text, (x+1.5*r,y+r))
        

        if self.rings:
            pygame.draw.circle(win,self.color,(x,y),r*1.2,width=int(r/10))

    def attraction(self, other):
        distance = sqrt((other.x - self.x )** 2 + (other.y - self.y) ** 2)
        if other.sun:
            self.distance_to_sun = distance
        force = self.G * self.mass * other.mass / distance**2
        theta = atan2(other.y - self.y, other.x - self.x)
        return cos(theta) * force, sin(theta) * force

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
    
    def year(self,other):
        if self.y==other.y:
            print(1)

def init():
    Sun=Planet(sun["name"],0,0,sun["radius"],COLORS[sun["color"]],sun["mass"],0,sun["rings"])
    Sun.sun=True
    Earth=Planet(earth["name"],earth["AU"]*Planet.AU,0,earth["radius"],COLORS[earth["color"]],earth["mass"],earth["initial_velo"],earth["rings"])
    Mars=Planet(mars["name"],mars["AU"]*Planet.AU,0,mars["radius"],COLORS[mars["color"]],mars["mass"],mars["initial_velo"],mars["rings"])
    Mercury=Planet(mercury["name"],mercury["AU"]*Planet.AU,0,mercury["radius"],COLORS[mercury["color"]],mercury["mass"],mercury["initial_velo"],mercury["rings"])
    Venus=Planet(venus["name"],venus["AU"]*Planet.AU,0,venus["radius"],COLORS[venus["color"]],venus["mass"],venus["initial_velo"],venus["rings"])
    Jupiter=Planet(jupiter["name"],jupiter["AU"]*Planet.AU,0,jupiter["radius"],COLORS[jupiter["color"]],jupiter["mass"],jupiter["initial_velo"],jupiter["rings"])
    Saturn=Planet(saturn["name"],saturn["AU"]*Planet.AU,0,saturn["radius"],COLORS[saturn["color"]],saturn["mass"],saturn["initial_velo"],saturn["rings"])
    Uranus=Planet(uranus["name"],uranus["AU"]*Planet.AU,0,uranus["radius"],COLORS[uranus["color"]],uranus["mass"],uranus["initial_velo"],uranus["rings"])
    Neptune=Planet(neptune["name"],neptune["AU"]*Planet.AU,0,neptune["radius"],COLORS[neptune["color"]],neptune["mass"],neptune["initial_velo"],neptune["rings"])
    return([Sun, Earth, Mars, Mercury, Venus,Jupiter,Saturn,Uranus,Neptune])

def main():
    run=True
    clock=pygame.time.Clock()
    Planets=init()
    while run:
        clock.tick(FPS)
        WIN.fill(COLORS["black"])

        for star in stars:
            pygame.draw.line(WIN,COLORS["white"], (star[0], star[1]), (star[0], star[1]))
            star[0]-=0.3*randint(0,2)
            star[1]-=0.1*randint(0,2)
            if star[0] < 0:
                star[0],star[1] = WIDTH,randint(0, HEIGHT)

        for planet in Planets:
            planet.update_position(Planets)
            planet.draw(WIN)

        unit_text = Planet.FONT.render("AU ( Astronomical Unit / Distance Sun-Earth ) = 150.000.000 Km ", 1, COLORS["white"])
        WIN.blit(unit_text, (WIDTH-unit_text.get_width()-20,unit_text.get_height()+20))

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and Planet.SCALE<(1500/Planet.AU):
                    Planet.SCALE*=1.2
                elif event.button == 5 and Planet.SCALE>(15/Planet.AU):
                    Planet.SCALE/=1.2

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            Planet.SIZE+=4
        elif keys[pygame.K_DOWN]:
            Planet.SIZE-=4
        elif keys[pygame.K_SPACE]:
            Planet.SIZE=1
            Planets=init()
        pygame.display.update()


    pygame.quit()

if __name__=='__main__':
    main()
