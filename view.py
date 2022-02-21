

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
        self.y = 1 * (y / 12)
        self.w = 4 * (x / 12)
        self.h = 10 * (y / 12)

        self.color = pygame.Color("blue")
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def set_red_pos(self) -> None:
        '''
        preset for a red button
        '''
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
        self.buttons.append(Button(self.screen))  # blue right
        self.buttons.append(Button(self.screen))  # red left
        self.buttons[1].set_red_pos()

    def update(self):
        if pygame.mouse.get_pressed()[0] and self.buttons[0].rect.collidepoint(pygame.mouse.get_pos()):
            if View.debug:
                print("blue right pressed", file=sys.stderr)
                self.take_choice_dict(True, View.pipe)

        if pygame.mouse.get_pressed()[0] and self.buttons[1].rect.collidepoint(pygame.mouse.get_pos()):
            if View.debug:
                print("red left pressed", file=sys.stderr)
                self.take_choice_dict(False, View.pipe)

    def draw(self):
        super().draw()
        for button in self.buttons:
            pygame.draw.rect(self.screen, button.color, button.rect)

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
        self.texts.append(Text(0, 0, 30, "", pygame.Color("white")))

    def update(self):
        super().update()
        self.texts[0].txt = f"Attente badge RFID  {datetime.datetime.today()}"
        for txt in self.texts:
            txt.update()

    def draw(self):
        super().draw()
        for txt in self.texts:
            txt.draw(self.screen)


class View:
    '''
    contain scene, pygame proprety,…
    '''
    debug = True
    pipe = dict()

    def __init__(self) -> None:
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
        pygame.init()

        
        
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
        self.screen.fill(pygame.Color("black"))
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

    def do_next_scene_dict(self, d: dict):
        '''
        change the current scene and change the reference of View.pipe
        '''
        print("do_next_scene_dict", file=sys.stderr)
        self.do_next_scene()
        View.pipe = d


class Text:
    def __init__(self, x: float, y: float, size: float, txt: str, color: pygame.Color) -> None:
        '''
        text with position, size and color
        '''
        self.txt = txt
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


if __name__ == "__main__":
    view = View()
    # view.load()
