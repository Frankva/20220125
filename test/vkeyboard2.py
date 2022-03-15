
import pygame
import pygame_vkeyboard as vkboard


def on_key_event(text):
    print('Current text:', text)


class App:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 480))
        self.screen.fill((20, 100, 100))

        self.layout = App.layout_CH()
        self.keyboard = vkboard.VKeyboard(self.screen, on_key_event,
            self.layout, renderer=vkboard.VKeyboardRenderer.DARK, 
            special_char_layout=App.layout_special(),
            show_text=True)

        self.clock = pygame.time.Clock()

    def load(self):
        while True:
            self.clock.tick(100)
            events = pygame.event.get()

            for event in events:
                #self.keyboard.on_event(event)
                if event.type == pygame.QUIT:
                    print('Average FPS: ', self.clock.get_fps())
                    exit()
            self.keyboard.update(events)
            self.screen.fill((20, 100, 100))
            rects = self.keyboard.draw(self.screen, force=True)
            #pygame.display.update(rects)
            pygame.display.flip()

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

def main():
    app = App()
    app.load()


if __name__ == '__main__':
    main()
