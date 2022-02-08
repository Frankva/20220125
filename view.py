import pygame

class Button:
    def __init__(self):
        x, y = view.screen.get_size()
        self.x = 7 * (x / 12)
        self.y = 1* (y / 12)
        self.w = 4 * (x / 12)
        self.h = 10 * (y / 12)
        
        self.color = pygame.Color("blue")
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
    def set_red_pos(self):
        print("set_red_pos")
        x, y = view.screen.get_size()
        self.color = pygame.Color("red")
        self.x = x / 12
        self.y = y / 12
        self.w = 4 * (x / 12)
        self.h = 10 * (y / 12)
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)


class View:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 400))#pygame.FULLSCREEN
        self.running = True
        self.buttons = list()
        

    def load(self):
        self.buttons.append(Button())
        self.buttons.append(Button())
        self.buttons[0].set_red_pos()
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