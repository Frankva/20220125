
from itertools import product
import pygame
import pygame_vkeyboard as vkboard
import sys
import os
import datetime


class Button:
    '''
    button show with rect and unique color
    '''

#    def __init__(self, screen: pygame.surfarray) -> None:
#        if View.debug:
#            print("Button.init", file=sys.stderr)
#        self.screen = screen
#        x, y = self.screen.get_size()
#        self.x = 7 * (x / 12)
#        self.y = 4 * (y / 12)
#        self.w = 4 * (x / 12)
#        self.h = 7 * (y / 12)
#
#        self.color = pygame.Color("#005BA9") # blue
#        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
#
    def __init__(self, screen: pygame.Surface, x, y, w, h,
                 color=pygame.Color("#6c767e"), img: str = 'cancel') -> None:
        print("Button.init", file=sys.stderr)
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.img = Loader.load_img(img, pygame.Color('#f8f9fa'))
        
       

    @staticmethod
    def inside_button(screen):

        cx, cy = screen.get_size()
        x = 7 * (cx / 12)
        y = 4 * (cy / 12)
        w = 4 * (cx / 12)
        h = 7 * (cy / 12)
        img = 'in'

        color = pygame.Color("#007bff")  # blue
        return Button(screen, x, y, w, h, color, img)

    @staticmethod
    def outside_button(screen):

        cx, cy = screen.get_size()
        x = 1 * (cx / 12)
        y = 4 * (cy / 12)
        w = 4 * (cx / 12)
        h = 7 * (cy / 12)
        img = 'out'

        color = pygame.Color("#Dc3545")  # red
        return Button(screen, x, y, w, h, color, img)

    @staticmethod
    def log_button(screen):
        cx, cy = screen.get_size()
        x = 9 * (cx / 12)
        y = 1 * (cy / 12)
        w = 2 * (cx / 12)
        h = 2 * (cy / 12)
        img = 'log'
        color = pygame.Color("#6c767e")  # gray
        return Button(screen, x, y, w, h, color, img)

    @staticmethod
    def cancel_button(screen):

        cx, cy = screen.get_size()
        x = 1 * (cx / 12)
        y = 1 * (cy / 12)
        w = 2 * (cx / 12)
        h = 2 * (cy / 12)
        img = 'cancel'

        color = pygame.Color("#6c767e")  # gray
        return Button(screen, x, y, w, h, color, img)

    @staticmethod
    def return_button(screen):

        cx, cy = screen.get_size()
        x = 1 * (cx / 12)
        y = 1 * (cy / 12)
        w = 2 * (cx / 12)
        h = 2 * (cy / 12)
        img = 'return'

        color = pygame.Color('#6c767e')  # off white 
        return Button(screen, x, y, w, h, color, img)

#    def set_red_pos(self) -> None:
#        '''
#        obselete
#        preset for a red button
#        '''
#        if View.debug:
#            print("Button.set_red_pos", file=sys.stderr)
#        x, y = self.screen.get_size()
#        self.color = pygame.Color("#DD1C1A") # red
#        self.x = 1 * x / 12
#        self.y = 4 * y / 12
#        self.w = 4 * (x / 12)
#        self.h = 7 * (y / 12)
#        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
#

 #   @classmethod
 #   def setting_button(cls):
 #
 #       return cls.__init__()
 #
    def draw(self, screen) -> None:
        pygame.draw.rect(screen, self.color, self.rect, 0, 10)
        self.draw_img_center(screen)
    
    def draw_img_center(self, screen):
        screen.blit(self.img, (self.x + self.w/2 - self.img.get_width()/2,
                               self.y + self.h/2 - self.img.get_height()/2))


class Scene:
    '''
    scene containt text and button
    '''

    def __init__(self, screen, view) -> None:
        if View.debug:
            print("init Scene", file=sys.stderr)

        self.screen = screen
        self.view = view

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


class SceneTime(Scene):
    def __init__(self, screen, view) -> None:
        super().__init__(screen, view)
        self.entry_time = datetime.datetime.today()

    def update(self) -> None:
        '''
        is called each frame
        '''
        super().update()
        self.do_cancel()

    def check_time(self, minute: int) -> bool:
        '''
        check time with now and entry_time proprety 
        '''
        return datetime.datetime.today() - self.entry_time >\
            datetime.timedelta(minutes=minute)

    def do_cancel(self) -> None:
        if self.check_time(1):
            self.view.cancel()

    def reset_entry_time(self) -> None:
        self.entry_time = datetime.datetime.today()


class SceneSelect(SceneTime):
    '''
    is the scene with buttons
    '''

    def __init__(self, screen, view):
        if View.debug:
            print("SceneSelect load", file=sys.stderr)
        super().__init__(screen, view)

        self.choice = dict()

        self.buttons = list()
        self.buttons.append(Button.inside_button(self.screen))  # blue right
        self.buttons.append(Button.outside_button(self.screen))  # red left
        self.buttons.append(Button.log_button(self.screen))  # red left
        self.buttons.append(Button.cancel_button(self.screen))  # red left
        #self.buttons[1].set_red_pos()
        self.texts = list()
        self.texts.append(Text(10, 5, 30, '', pygame.Color('black')))

    def update(self):
        super().update()
        self.do_press_button()
        try:
            # must be optimised, not all frame
            self.texts[0](View.pipe['surname'] + ' ' + View.pipe['name'])
        except not KeyboardInterrupt:
            pass

    def do_press_button(self):
        if self.buttons[0].rect.collidepoint(pygame.mouse.get_pos()) and\
                self.view.mouse.release('left'):
            if View.debug:
                print("blue right pressed", file=sys.stderr)
            self.take_choice_dict(True, View.pipe)

        if self.buttons[1].rect.collidepoint(pygame.mouse.get_pos()) and\
                self.view.mouse.release('left'):
            if View.debug:
                print("red left pressed", file=sys.stderr)
            self.take_choice_dict(False, View.pipe)

        if self.buttons[2].rect.collidepoint(pygame.mouse.get_pos()) and\
                self.view.mouse.release('left'):
            self.reset_entry_time()
            # access parent instance
            self.view.do_log_scene(View.pipe['log'])

        if self.buttons[3].rect.collidepoint(pygame.mouse.get_pos()) and\
                self.view.mouse.release('left'):
            # access parent instance
            self.view.cancel()

    def draw(self):
        super().draw()
        for button in self.buttons:
            #pygame.draw.rect(self.screen, button.color, button.rect)
            button.draw(self.screen)
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

    def __init__(self, screen, view):

        super().__init__(screen, view)

        self.texts = list()
        self.texts.append(Text(10, 10, 30, "Attente d’un badge RFID"))
        self.texts.append(Text(10, 40, 30, ""))

    def update(self):
        super().update()
        self.texts[1].text = str(datetime.datetime.today())[0:-7]
        for txt in self.texts:
            txt.update()

    def draw(self):
        super().draw()
        for txt in self.texts:
            txt.draw(self.screen)


class SceneLog(SceneTime):
    '''
    scene show logs
    '''

    def __init__(self, screen, view) -> None:
        super().__init__(screen, view)
        self.texts = list()
        #nb_log = 10
        self.size_text = 30
#        for i in range(nb_log):
#            self.texts.append(Text(0, 0, size_txt + size_txt * i, "", pygame.Color('black')))

        self.buttons = list()
        self.buttons.append(Button.return_button(screen))
        cx, cy = screen.get_size()
        self.buttons.append(Button(screen, 9 * cx / 12, 1 * cy / 12,
                                   2 * cx / 12, 2 * cy / 12, img='more'))

    def set_text(self, logs: list):
        print('SceneLog.set_text')
        cx, cy = self.screen.get_size()
        x = 1 * cx / 12
        y = 4 * cy / 12
        self.texts = list()
        text_inside = 'entrée'
        text_outside = 'sortie'
        for index, log in enumerate(logs):
            text_log = str(log['date'])[:-3] + ' ' + self.change_text_bool(
                log['inside'], text_inside, text_outside)
            self.texts.append(Text(x, y + index * self.size_text,
                              self.size_text, text_log, pygame.Color('black')))

    @staticmethod
    def change_text_bool(b, text_true: str, text_false: str):
        return text_true if bool(b) else text_false

    def update(self):
        super().update()
        self.do_press_button()

    def do_press_button(self):
        if self.view.mouse.release('left') and\
                self.buttons[0].rect.collidepoint(pygame.mouse.get_pos()):
            self.reset_entry_time()
            # access parent instance
            self.view.current_scene = 'select'
            # add reset timer

        if self.view.mouse.release('left') and\
                self.buttons[1].rect.collidepoint(pygame.mouse.get_pos()):
            self.reset_entry_time()
            # access parent instance
            self.view.do_work_time()
            # self.view.current_scene = 'time'
            # add reset timer


    def draw(self):
        super().draw()
        for text in self.texts:
            text.draw(self.screen)

        for button in self.buttons:
            button.draw(self.screen)

class SceneWorkTime(SceneTime):
    def __init__(self, screen, view) -> None:
        super().__init__(screen, view)
        self.texts = list()
        self.size_text = 30
        self.buttons = list()
        self.buttons.append(Button.return_button(screen))

    def do_press_button(self) -> None:
        if self.view.mouse.release('left') and\
                self.buttons[0].rect.collidepoint(pygame.mouse.get_pos()):
            self.reset_entry_time()
            # access parent instance
            self.view.current_scene = 'log'
            # add reset timer

    def set_text(self):
        print('SceneWorkTime.set_text')
        cx, cy = self.screen.get_size()
        x = 1 * cx / 12
        y = 4 * cy / 12
        self.texts = list()
        self.texts.append(Text(x, y, self.size_text, ''))
        self.texts.append(Text(x, y + self.size_text, self.size_text, ''))
        self.texts.append(Text(x, y + 2 * self.size_text, self.size_text, ''))
        self.texts[0]('Temps de présence : ')
        try:
            self.texts[1]('semaine passée : ' + str(View.pipe['time_last_week']))
            self.texts[2]('semaine en cours : ' + \
                str(View.pipe['time_current_week']))
        except KeyError:
            pass

    def update(self):
        super().update()
        self.do_press_button()

    def draw(self):
        super().draw()
        for text in self.texts:
            text.draw(self.screen)

        for button in self.buttons:
            button.draw(self.screen)


class SceneModal(SceneTime):
    '''
    scene with one text and one button
    '''

    def __init__(self, screen, view, text: str, next_scene: str) -> None:
        super().__init__(screen, view)
        self.size_text = 20
        cx, cy = screen.get_size()
        self.text = Text(1 * cx / 12, 1 * cx / 12, self.size_text, text,
                         pygame.Color('black'))
        self.button = Button(self.screen, 4 * cx / 12, 8 * cy / 12,
                             3 * cx / 12, 3 * cy / 12, img='confirm')
        self.next_scene = next_scene

    def update(self):
        super().update()
        self.do_press_button()

    def draw(self):
        super().draw()
        self.text.draw(self.screen)
        self.button.draw(self.screen)

    
    def do_press_button(self):
        if self.view.mouse.release('left') and \
                self.button.rect.collidepoint(pygame.mouse.get_pos()):
            self.reset_entry_time()
            self.view.current_scene = self.next_scene


class SceneKeyboard(SceneTime):
    '''
    scene with keyboard and two buttons
    '''

    def __init__(self, screen, view) -> None:
        super().__init__(screen, view)
        self.layout = self.layout_CH()
        cx, cy = screen.get_size()

        self.buttons = list()
        self.buttons.append(
            Button(self.screen, 1 * cx / 12, 0.2 * cy / 12, 1 * cx / 12,
                   1 * cy / 12))
        self.buttons.append(
            Button(self.screen, 10 * cx / 12, 0.2 * cy / 12, 1 * cx / 12,
                   1 * cy / 12, img='confirm'))
        self.keyboard = vkboard.VKeyboard(self.screen, self.on_key_event,
            self.layout, renderer=vkboard.VKeyboardRenderer.DARK, 
            special_char_layout=self.layout_special(),
            show_text=True)
        self.twice = False 

    def on_key_event(self, text):
        print('Current text:', text)
        self.reset_entry_time()

    def do_press_button(self):
        if self.buttons[0].rect.collidepoint(pygame.mouse.get_pos()) and\
                self.view.mouse.release('left'):
            # access parent instance
            self.view.cancel()
        if self.buttons[1].rect.collidepoint(pygame.mouse.get_pos()) and\
                self.view.mouse.release('left'):
            # access parent instance
            if not self.twice:
                self.twice = True
                self.view.do_unknown_badge(True)
            else:
                View.current_scene = 'select'
                self.twice = False


    def update(self):
        super().update()
        self.keyboard.update(self.view.events)
        self.do_press_button()

    def draw(self):
        super().draw()
        self.keyboard.draw(self.screen, force=True)
        for button in self.buttons:
            button.draw(self.screen)
        
    @staticmethod
    def layout_CH():
        model = [
            'qwertzuiop',
            'asdfghjkl',
            'yxcvbnm'
        ]
        return vkboard.VKeyboardLayout(model, height_ratio=9/12)

    @staticmethod
    def layout_special():
        model = [
            '-áàâæãåäąç',
            'ĉćčďéèêëęě',
            'ĝğîĥïíìįĵł',
            'ñńöôœðûüùÿ'
        ]
        return vkboard.VKeyboardLayout(model, height_ratio=9/12)


class Mouse:
    def __init__(self) -> None:
        self.left = False
        self.old_left = False

    def update(self, events):
        # self.event = event
        # self.old_left = self.left
        # self.left = pygame.mouse.get_pressed()[0] or (pygame.FINGERDOWN == 
        # self.event)
        self.old_left = self.left
        # self.left = pygame.mouse.get_pressed()[0] or (pygame.FINGERUP in 
        # event)
        for event in events:
            if (pygame.MOUSEBUTTONDOWN == event.type) or (pygame.FINGERDOWN == 
            event.type):
                self.left = True
            elif (pygame.MOUSEBUTTONUP == event.type) or (pygame.FINGERUP == 
            event.type):
                self.left = False
        
    def release(self, button: str):
        '''
        detect release click
        up click
        
        '''
        return (not getattr(self, button)) and (getattr(self, f"old_{button}"))


class View:
    '''
    contain scene, pygame proprety,…
    '''
    debug = True

    pipe = dict()

    def __init__(self, pipe=None) -> None:
        self.running = True

        self.scenes = dict()
        self._current_scene = "wait"
        if pipe != None:
            View.pipe = pipe

    def load_pygame(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        if os.name != "nt":
            self.screen = pygame.display.set_mode(
                (800, 480), pygame.FULLSCREEN)
            pygame.mouse.set_visible(False)
        else:
            self.screen = pygame.display.set_mode((800, 480))
        pygame.display.set_caption("Timbreuse")
        self.events = pygame.event.get()
        self.mouse = Mouse()
        self.background_color = pygame.Color('#ffffff')

    def load(self) -> None:
        '''
        start pygame loop
        '''
        self.load_pygame()
        self.load_scene()
        while self.running:
            if View.debug:
                #print("loop", file=sys.stderr)
                pass
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False
            self.update()
            self.draw()
        pygame.quit()

    def load_scene(self) -> None:
        self.scenes["wait"] = SceneWait(self.screen, self)
        self.scenes["select"] = SceneSelect(self.screen, self)
        self.scenes["log"] = SceneLog(self.screen, self)
        self.scenes["time"] = SceneWorkTime(self.screen, self)
        self.scenes["keyboard"] = SceneKeyboard(self.screen, self)

    def __del__(self) -> None:
        pygame.quit()
        sys.exit()

    def update(self) -> None:
        '''
        is called each frame
        '''
        self.clock.tick(60)
        self.mouse.update(self.events)
        self.scenes[self.current_scene].update()
        self.debug_command()

    def debug_command(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.running = False

        if pygame.key.get_pressed()[pygame.K_j]:
            # change scene ;  debug

            self.do_select_scene()

        if pygame.key.get_pressed()[pygame.K_k]:
            # change scene ;  debug

            self.do_log_scene(View.pipe['log'])

        if pygame.key.get_pressed()[pygame.K_l]:
            # change scene ;  debug
            self.do_unknown_badge()

    def draw(self) -> None:
        '''
        is called each frame. containt fonction to show
        '''
        self.screen.fill(self.background_color)
        self.scenes[self.current_scene].draw()
        pygame.display.flip()

    @property
    def current_scene(self) -> Scene:
        return self._current_scene

    @current_scene.setter
    def current_scene(self, newScene: str) -> None:
        print('current_scene.setter', self._current_scene, newScene,
              file=sys.stderr)

        if newScene in self.scenes.keys():
            self._current_scene = newScene
            if isinstance(self.scenes[newScene], SceneTime):
                self.scenes[newScene].reset_entry_time()
        else:
            print(self.scenes.keys(), file=sys.stderr)
            raise ValueError(f"scene {newScene} does not exist")

    def do_select_scene(self) -> None:
        '''
        change the current scene
        '''

        print("do_next_scene", file=sys.stderr)
        if self.current_scene != "select":
            self.current_scene = "select"
        else:
            self.current_scene = "wait"

    def do_select_scene_dict(self, pipe: dict):
        '''
        change the current scene and change the reference of View.pipe
        '''
        print("do_next_scene_dict", file=sys.stderr)
        self.do_select_scene()
        View.pipe = pipe

    def do_log_scene(self, log) -> None:
        if self.current_scene == 'select':
            self.current_scene = 'log'
            self.scenes['log'].set_text(log)

    def do_work_time(self) -> None:
        if self.current_scene == 'log':
            self.current_scene = 'time'
            self.scenes['time'].set_text()

    def do_unknown_badge(self, twice=False):
        if not twice:
            text = "Le badge est inconnue. Veuille taper votre nom de famille."
        else:
            text = "Veuille taper votre prénom."

        self.scenes['modal'] = SceneModal(self.screen, self, text, 'keyboard')
        self.current_scene = 'modal'

    def cancel(self):
        '''
        when time expire or press quit button
        '''
        self.current_scene = 'wait'
        self.load_scene()
        View.pipe['cancel'] = True


class Text:
    def __init__(self, x: float, y: float, size: float, text: str,
                 color: pygame.Color=pygame.Color('#212529')) -> None:
        '''
        text with position, size and color
        '''
        self.__text = text
        self.pos = pygame.math.Vector2(x, y)
        self.size = size
        self.font = Loader.load_txt('liberation', self.size)
        self.color = color
        self.img = self.font.render(self.text, True, self.color)

    def update(self) -> None:
        '''
        is called each frame
        '''
        self.img = self.font.render(self.text, True, self.color)

    def draw(self, screen: pygame.Surface) -> None:
        '''
        is called each frame. containt function to show
        '''
        screen.blit(self.img, self.pos)

    def __str__(self) -> str:
        return self.text

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, txt: str):
        if isinstance(txt, str):
            self.__text = txt
        else:
            raise ValueError("'must be str")

    def __call__(self, text):
        self.text = text
        self.update()
    
    
class Loader:
    '''
    load file 
    '''
    paths = dict()
    paths['cancel'] = 'icons/x.bmp'
    paths['liberation'] = 'fonts/LiberationSans-Regular.ttf'
    paths['in'] = 'icons/arrow-up.bmp'
    paths['out'] = 'icons/arrow-down.bmp'
    paths['log'] = 'icons/clock-history.bmp'
    paths['return'] = 'icons/arrow-left.bmp'
    paths['more'] = 'icons/three-dots.bmp'
    paths['confirm'] = 'icons/check.bmp'
    

    @classmethod
    def load_img(cls, name:str, color:pygame.Color=None):
        print('Loader.load', file=sys.stderr)
        if color is None:
            return pygame.image.load(cls.paths[name])
        else:
            
            return cls.change_color(pygame.image.load(cls.paths[name]), color)
        #return cls.change_color(pygame.image.load(cls.paths[name]),
        #                        pygame.Color('#dc3545')).convert_alpha()
    
    @classmethod
    def load_txt(cls, name, size):
        print('load_txt', file=sys.stderr)
        return pygame.font.Font(cls.paths[name], size)
    
    def change_color(img: pygame.Surface, color: pygame.Color):
        w, h = img.get_size()
        r, g, b, _ = color
        for x, y in product(range(w), range(h)):
           alpha = img.get_at((x,y))[3]
           img.set_at((x, y), pygame.Color(r, g, b, alpha))
        return img


def test1():
    # test value
    pipe = dict()
    pipe['name'] = 'Bob'
    pipe['surname'] = 'Leta'
    pipe['log'] = list()
    pipe['log'].append(dict())
    pipe['log'].append(dict())
    pipe['log'][0]['date'] = datetime.datetime(2022, 2, 18, 15, 28, 49)
    pipe['log'][1]['date'] = datetime.datetime(2022, 1, 19, 16, 30, 51)
    pipe['log'][0]['inside'] = True
    pipe['log'][1]['inside'] = False
    pipe['time_last_week'] = datetime.timedelta(seconds=20212)
    pipe['time_current_week'] = datetime.timedelta(seconds=307)
    view = View(pipe)
    view.load()


def main():
    view = View()
    view.load()


if __name__ == "__main__":
    mode = 1
    if mode == 0:
        main()
    elif mode == 1:
        test1()
