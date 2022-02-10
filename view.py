
from distutils.log import debug
import pygame
import sys
import os
import datetime

class Button:
    def __init__(self, screen):
        if View.debug:
            print("Button.init", file=sys.stderr)
        self.screen = screen
        x, y = self.screen.get_size()
        self.x = 7 * (x / 12)
        self.y = 1* (y / 12)
        self.w = 4 * (x / 12)
        self.h = 10 * (y / 12)
        
        self.color = pygame.Color("blue")
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def set_red_pos(self):
        if View.debug:
            print("Button.set_red_pos", file=sys.stderr)
        x, y = self.screen.get_size()
        self.color = pygame.Color("red")
        self.x = x / 12
        self.y = y / 12
        self.w = 4 * (x / 12)
        self.h = 10 * (y / 12)
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        

class Scene:
    def __init__(self, screen):
        if View.debug:
            print("init Scene", file=sys.stderr)
        self.font = pygame.font.SysFont(None, 24)
        self.screen = screen

    def update(self):
        pass

    def draw(self, screen):
        pass

class SceneSelect(Scene):
    def __init__(self, screen):
        if View.debug:
            print("SceneSelect load", file=sys.stderr)
        super().__init__(screen)

        self.choice = dict()
       

        self.buttons = list()
        self.buttons.append(Button(self.screen)) # blue right
        self.buttons.append(Button(self.screen)) # red left
        self.buttons[1].set_red_pos()
    
    def update(self):
        if pygame.mouse.get_pressed()[0] and self.buttons[0].rect.collidepoint(pygame.mouse.get_pos()):
            if View.debug:
                print("blue right pressed", file=sys.stderr)
                self.take_choice_dict(True, View.stream)

        
        if pygame.mouse.get_pressed()[0] and self.buttons[1].rect.collidepoint(pygame.mouse.get_pos()):
            if View.debug:
                print("red left pressed", file=sys.stderr)
                self.take_choice_dict(False, View.stream)




    def draw(self, screen):
        super().draw(screen)
        for button in self.buttons:
            pygame.draw.rect(screen, button.color, button.rect)

    @staticmethod
    def take_choice(choice):

        return  (choice, datetime.datetime.today())
    @classmethod
    def take_choice_dict(cls, choice, dict):
        '''
        get the choice in a dict in args
        '''
        dict["in"], dict["time"] = cls.take_choice(choice)



            
class SceneWait(Scene):
    def __init__(self, screen):
        
        super().__init__(screen)
        self.texts = list()
        self.texts.append(self.font.render(f"Attente badge RFID", True, pygame.Color("white")))

    def update(self):
        super().update()
        self.texts[0] = self.font.render(f"Attente badge RFID  {datetime.datetime.today()}", True, pygame.Color("white"))

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.texts[0], (0,0))

class View:
    debug = True
    stream = dict()
    def __init__(self):
        pygame.init()
        if os.name != "nt":
            self.screen = pygame.display.set_mode((800, 400),pygame.FULLSCREEN)#pygame.FULLSCREEN
        else:
            self.screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption("test")
        self.running = True
        
        self.scenes = dict()
        self._current_scene = "wait"

        self.load()

    def load(self):
        '''
        start pygame loop
        '''
        self.scenes["wait"] = SceneWait(self.screen)
        self.scenes["select"] = SceneSelect(self.screen)

        while self.running:
            if View.debug:
                print("loop", file=sys.stderr)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.update()
            self.draw()
        pygame.quit()

    def __del__(self):
        pygame.quit()
        sys.exit()

    def update(self):
        
        self.scenes[self.current_scene].update()

        

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.running = False

        if pygame.key.get_pressed()[pygame.K_j]:
            #change scene ;  debug

            if self.current_scene != "select":
                self.current_scene = "select"
            else:
                self.current_scene = "wait"

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
            self._current_scene = newScene
        else:
            print(self.scenes.keys(), file=sys.stderr)
            raise ValueError(f"scene {newScene} does not exist")

    
if __name__ == "__main__":
    view = View()
    #view.load()