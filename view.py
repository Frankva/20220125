

import re
import pygame
import sys
import os
import datetime


class Button:
    '''
    button show with rect and unique color
    '''

    def __init__(self, screen: pygame.surfarray) -> None:
        if View.debug:
            print("Button.init", file=sys.stderr)
        self.screen = screen
        x, y = self.screen.get_size()
        self.x = 7 * (x / 12)
        self.y = 4 * (y / 12)
        self.w = 4 * (x / 12)
        self.h = 7 * (y / 12)

        self.color = pygame.Color("#005BA9") # blue
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
    
    def __init__(self, screen: pygame.surfarray, x, y, w, h, color) -> None:
        if View.debug:
            print("Button.init", file=sys.stderr)
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    @staticmethod
    def inside_button(screen):
        
        cx, cy = screen.get_size()
        x = 7 * (cx / 12)
        y = 4 * (cy / 12)
        w = 4 * (cx / 12)
        h = 7 * (cy / 12)

        color = pygame.Color("#005BA9") # blue
        return Button(screen, x, y, w, h, color)
   
    @staticmethod
    def outside_button(screen):
        
        cx, cy = screen.get_size()
        x = 1 * (cx / 12)
        y = 4 * (cy / 12)
        w = 4 * (cx / 12)
        h = 7 * (cy / 12)

        color = pygame.Color("#DD1C1A") # red
        return Button(screen, x, y, w, h, color)
   
    def set_red_pos(self) -> None:
        '''
        preset for a red button
        '''
        if View.debug:
            print("Button.set_red_pos", file=sys.stderr)
        x, y = self.screen.get_size()
        self.color = pygame.Color("#DD1C1A") # red
        self.x = 1 * x / 12
        self.y = 4 * y / 12
        self.w = 4 * (x / 12)
        self.h = 7 * (y / 12)
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    @classmethod
    def setting_button(cls):
        return cls.__init__()


class Scene:
    '''
    scene containt text and button
    '''
    def __init__(self, screen) -> None:
        if View.debug:
            print("init Scene", file=sys.stderr)

        self.screen = screen

    def update(self) -> None:
        '''
        is called each frame
        '''
        pass

    def draw(self) -> None:
        '''
        is called each frame. containt function to show
        '''
        pass


class SceneSelect(Scene):
    '''
    is the scene with buttons
    '''
    def __init__(self, screen):
        if View.debug:
            print("SceneSelect load", file=sys.stderr)
        super().__init__(screen)

        self.choice = dict()

        self.buttons = list()
        self.buttons.append(Button.inside_button(self.screen))  # blue right
        self.buttons.append(Button.outside_button(self.screen))  # red left
        #self.buttons[1].set_red_pos()
        self.texts = list()
        self.texts.append(Text(0, 0, 31, '', pygame.Color('black')))


    def update(self):
        super().update()
        if pygame.mouse.get_pressed()[0] and self.buttons[0].rect.collidepoint(pygame.mouse.get_pos()):
            if View.debug:
                print("blue right pressed", file=sys.stderr)
                self.take_choice_dict(True, View.pipe)

        if pygame.mouse.get_pressed()[0] and self.buttons[1].rect.collidepoint(pygame.mouse.get_pos()):
            if View.debug:
                print("red left pressed", file=sys.stderr)
                self.take_choice_dict(False, View.pipe)
        self.texts[0](View.pipe['surname'] + ' ' + View.pipe['name']) # must be optimised, not all frame


    def draw(self):
        super().draw()
        for button in self.buttons:
            pygame.draw.rect(self.screen, button.color, button.rect)
        for text in self.texts:
            text.draw(self.screen)

    @staticmethod
    def take_choice(choice: bool) -> tuple:
        '''
        return arg and date time
        '''
        return (choice, datetime.datetime.today())

    @classmethod
    def take_choice_dict(cls, choice, dict) -> None:
        '''
        get the choice in a dict in args
        '''
        dict["inside"], dict["date"] = cls.take_choice(choice)


class SceneWait(Scene):
    '''
    is the waiting screen with time
    '''
    def __init__(self, screen):

        super().__init__(screen)

        self.texts = list()
        self.texts.append(Text(0, 0, 30, "", pygame.Color("#001B33")))

    def update(self):
        super().update()
        self.texts[0].txt = f"Attente badge RFID  {datetime.datetime.today()}"
        for txt in self.texts:
            txt.update()

    def draw(self):
        super().draw()
        for txt in self.texts:
            txt.draw(self.screen)

class SceneLog(Scene):
    '''
    scene show logs
    '''
    def __init__(self, screen) -> None:
        super().__init__(screen)
        self.texts = list()
        nb_log = 10
        size_txt = 30
        for i in range(nb_log):
            self.texts.append(Text(0, 0, size_txt + size_txt * i, "", pygame.Color('black')))

    def update(self):
        super().update()

    def draw(self):
        super().draw()


class View:
    '''
    contain scene, pygame proprety,…
    '''
    debug = True
    pipe = dict()
    pipe['name'] = 'Name'
    pipe['surname'] = 'Surname'
    pipe['log'] = dict()

    def __init__(self) -> None:
        pygame.init()

        if os.name != "nt":
            self.screen = pygame.display.set_mode(
                (800, 400), pygame.FULLSCREEN)  # pygame.FULLSCREEN
        else:
            self.screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption("test")
        self.running = True

        self.scenes = dict()
        self._current_scene = "wait"

        self.load()

    def load(self) -> None:
        '''
        start pygame loop
        '''
        self.scenes["wait"] = SceneWait(self.screen)
        self.scenes["select"] = SceneSelect(self.screen)

        while self.running:
            if View.debug:
                #print("loop", file=sys.stderr)
                pass
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.update()
            self.draw()
        pygame.quit()

    def __del__(self) -> None:
        pygame.quit()
        sys.exit()

    def update(self) -> None:
        '''
        is called each frame
        '''
        self.scenes[self.current_scene].update()

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.running = False

        if pygame.key.get_pressed()[pygame.K_j]:
            # change scene ;  debug

            self.do_next_scene()

    def draw(self) -> None:
        '''
        is called each frame. containt fonction to show
        '''
        self.screen.fill(pygame.Color("#DBCEB1"))
        self.scenes[self.current_scene].draw()
        pygame.display.flip()

    @property
    def current_scene(self) -> Scene:
        return self._current_scene

    @current_scene.setter
    def current_scene(self, newScene: str) -> None:

        if newScene in self.scenes.keys():
            self._current_scene = newScene
        else:
            print(self.scenes.keys(), file=sys.stderr)
            raise ValueError(f"scene {newScene} does not exist")

    def do_next_scene(self) -> None:
        '''
        change the current scene
        '''

        print("do_next_scene", file=sys.stderr)
        if self.current_scene != "select":
            self.current_scene = "select"
        else:
            self.current_scene = "wait"

    def do_next_scene_dict(self, dict: dict):
        '''
        change the current scene and change the reference of View.pipe
        '''
        print("do_next_scene_dict", file=sys.stderr)
        self.do_next_scene()
        View.pipe = dict


class Text:
    def __init__(self, x: float, y: float, size: float, txt: str, color: pygame.Color) -> None:
        '''
        text with position, size and color
        '''
        self.__txt = txt
        self.pos = pygame.math.Vector2(x, y)
        self.size = size
        self.font = pygame.font.SysFont("Arial", self.size)
        self.color = color
        self.img = self.font.render(self.txt, True, self.color)
        print(self.font)

    def update(self) -> None:
        '''
        is called each frame
        '''
        self.font = pygame.font.SysFont(None, self.size)
        self.img = self.font.render(self.txt, True, self.color)

    def draw(self, screen: pygame.Surface) -> None:
        '''
        is called each frame. containt function to show
        '''
        screen.blit(self.img, self.pos)

    def __str__(self) -> str:
        return self.txt
    
    @property
    def txt(self) -> str:
        return self.__txt
    
    @txt.setter
    def txt(self, txt: str):
        if isinstance(txt, str):
            self.__txt = txt
        else:
            raise ValueError("'must be str")
        
    def __call__(self, txt):
        self.txt = txt
        self.update()
    
        


def test1():
    view = View()

if __name__ == "__main__":
    # view = View()
    # view.load()
    test1()
