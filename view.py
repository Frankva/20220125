import pygame

class Button:
    def __init__(self):
        x, y = view.screen.get_size()
        self.x = x / 2
        self.y = y / 2
        self.w = x / 3
        self.h = y / 3
        
        self.color = pygame.Color("blue")
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
    def set_red_pos(self):



class View:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 400), pygame.FULLSCREEN)#pygame.FULLSCREEN
        self.running = True
        self.buttons = list()
        

    def load(self):
        self.buttons.append(Button())
        pygame.display.set_caption("test")
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.update()
                self.draw()
        pygame.quit()

    def __del__(self):
        pygame.quit()

    def update(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.running = False

    def draw(self):
        self.screen.fill(pygame.Color("black"))
        for button in self.buttons:
            pygame.draw.rect(self.screen, button.color, button.rect)
        pygame.display.flip()

view = View()
view.load()