from Segment import *

class Snake():
    body,turns = [],{}
    
    def __init__(self, color, pos):
        self.color = color
        self.head,self.dirnx,self.dirny = Segment(pos),0,1
        self.body.append(self.head)
    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx,self.dirny=-1,0
                elif keys[pygame.K_RIGHT]:
                    self.dirnx,self.dirny=1,0
                elif keys[pygame.K_UP]:
                    self.dirnx,self.dirny=0,-1
                elif keys[pygame.K_DOWN]:
                    self.dirnx,self.dirny=0,1
                self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx,c.dirny)
        
        
    def reset(self,pos):
        self.head,self.body,self.turns,self.dirnx,self.dirny = Segment(pos),[],{},0,1
        self.body.append(self.head)
        self.addSegment()

    def addSegment(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        if dx == 1 and dy == 0:
            self.body.append(Segment((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Segment((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Segment((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(Segment((tail.pos[0],tail.pos[1]+1)))
        self.body[-1].dirnx,self.body[-1].dirny = dx,dy
    
    def draw(self, win,width,rows):
        for i,c in enumerate(self.body):
            if i == 0:
                c.draw(win,width,rows,True)
            else:
                c.draw(win,width,rows)