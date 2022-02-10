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

class Scene:
    def __init__(self):
        print("init Scene")
        self.font = pygame.font.SysFont(None, 24)

class SceneSelect(Scene):
    def __init__(self):
        
        super().__init__()
        self.buttons = list()
        print("SceneSelect load")
        self.buttons.append(Button())
        self.buttons.append(Button())
        self.buttons[1].set_red_pos()
   


    def draw(self, screen):
        
        for button in self.buttons:
            pygame.draw.rect(screen, button.color, button.rect)
            
class SceneWait(Scene):
    def __init__(self):
        
        super().__init__()
        self.texts = list()
        self.texts.append(self.font.render("Attente badge RFID", True, pygame.Color("white")))


    def draw(self, screen):
        screen.blit(self.texts[0], (0,0))

class View:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 400))#pygame.FULLSCREEN
        self.running = True
        
        self.scenes = dict()
        self._current_scene = "wait"

    def load(self):
        self.scenes["wait"] = SceneWait()
        self.scenes["select"] = SceneSelect()
       
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
        self.scenes[self.current_scene].draw(self.screen)
        pygame.display.flip()

    @property
    def current_scene(self):
        return self._current_scene

    @current_scene.setter
    def current_scene(self, newScene):
        if newScene in self.scenes.keys():
            self.current_scene = newScene
        else:
            raise ValueError("scene in arg doos not exist")

    
if __name__ == "__main__":
    view = View()
    view.load()