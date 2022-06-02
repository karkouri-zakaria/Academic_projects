from matplotlib.pyplot import polar
import pygame
from math import hypot,atan2,sin,cos,pi
pygame.init()

WIDTH, HEIGHT, FPS = 600, 600, 30
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Fluid simulation")

x_units, y_units = 8, 8
hwidth, hheight = WIDTH / 2, HEIGHT / 2
x_scale, y_scale = WIDTH / x_units, HEIGHT / y_units
x_stop = x_units / 2; x_start = -x_stop
y_stop = y_units / 2; y_start = -y_stop

function = lambda x, y: (sin(2*y), -x/2)

def text(winace, position, text, size, color):
    winace.blit(pygame.font.SysFont("arial", size).render(text, 1, color), position)

def safe_drange(start, stop, step=1, precision=2):
    scaler = 10 ** precision
    start, stop, step = start * scaler, stop * scaler, step * scaler
    for i in range(int(start), int(stop), int(step)):
        yield i / scaler

def translate_and_scale(x, y):
    return (x * x_scale) + hwidth, hheight - (y * y_scale)

def draw_arrow(A, B, color, width=2):
    polar = lambda r, theta: (r * cos(theta), r * sin(theta))

    dy, dx = A[1] - B[1], A[0] - B[0]
    angle = atan2(dy, dx)
    mang = (angle + 2*pi) / 2*pi if angle < 0 else angle / 2*pi
    color = (0, 255-200 * mang, 255-200 * mang)
    
    dist = hypot(dx, dy) / 5 
    x1, y1 = polar(dist, angle + pi/4)
    x2, y2 = polar(dist, angle - pi/4)
    #pygame.draw.line(WIN, color, A, B, width)
    #pygame.draw.line(WIN, color, B, (B[0] + x1, B[1] + y1), width)
    #pygame.draw.line(WIN, color, B, (B[0] + x2, B[1] + y2), width)

class VectorField():

    def __init__(self, function, vecs_per_unit=2, color=(255, 0, 0)):
        self.function, self.vecs_per_unit, self.color = function, vecs_per_unit, color
        self.step = 1 / self.vecs_per_unit
        self._generate_vectors()

    def _generate_vectors(self):
        self.vectors = []
        for x in safe_drange(x_start, x_stop, self.step):
            for y in safe_drange(y_start, y_stop, self.step):
                try:
                    dx, dy = self.function(x, y)
                    self.vectors.append((x, y, x + dx / 8, y + dy / 8))
                except ZeroDivisionError:
                    continue

    def draw(self, surf):
        for vector in self.vectors:
            draw_arrow(translate_and_scale(vector[0], vector[1]), translate_and_scale(vector[2], vector[3]), self.color, surf)

class Particle():

    def __init__(self, function, x, y, color=(255, 0, 0), speed_scale=35):
        self.function, self.x, self.vy, self.color, self.speed_scale = function, x, y, color, speed_scale
        self.initial_speed = 1 / self.speed_scale

    def move(self):
        try:
            dx, dy = self.function(self.x, self.y)
        except ZeroDivisionError:
            dx, dy = 0, 0
        self.x += dx / self.speed_scale
        self.y += dy / self.speed_scale

    def draw(self):
        center = translate_and_scale(self.x, self.y)
        pygame.draw.circle(WIN, self.color, (int(center[0]), int(center[1])), 2)

    def update(self):
        self.move()
        self.draw()

def generate_particles(function):
    v = VectorField(function, vecs_per_unit=4)
    particles = []
    step = 0.1 * (((x_units + y_units) // 2) / 8)
    for x in safe_drange(x_start, x_stop, step):
        for y in safe_drange(y_start, y_stop, step):            
            particles.append(Particle(function, x, y))
    return v, particles

def main(run=True):

    Clock=pygame.time.Clock()
    pygame.key.set_repeat(100, 50)
    v, particles = generate_particles(function);
    WIN.fill((255,255,255))
    v.draw(WIN)

    while run:
        Clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

    pygame.Surface.blit(WIN, (0, 0));
    for p in particles:
        p.update();
    pygame.draw.rect(WIN, (255,255,255), (10, 10, 200, 28));
    text(WIN, (10, 10), "Swirl points", 25, (0,0,0));
    pygame.display.flip();    
    
    pygame.quit()

if __name__=="__main__":
    main()