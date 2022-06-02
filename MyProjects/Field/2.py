import pygame

pygame.init()
W,H,FPS=400,400,60
WIN=pygame.display.set_mode((W,H))
pygame.display.set_caption("main")


        
def main(run=True):
    Clock=pygame.time.Clock()
    F=feild()
    while run:
        Clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    pygame.quit()
if __name__=="__main__":
    main()