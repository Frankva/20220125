import pygame
import pygame_vkeyboard


def on_key_event(text):
    print('Current text:', text)


class App:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((500, 400))

        self.layout = pygame_vkeyboard.VKeyboardLayout(
            App.layout_CH(), height_ratio=1)
        
        print(pygame_vkeyboard.VKeyboardLayout.QWERTY)

        self.keyboard = pygame_vkeyboard.VKeyboard(self.screen, on_key_event,
                                                   self.layout)

        self.clock = pygame.time.Clock()

    def load(self):
        while True:
            self.clock.tick(100)

            for event in pygame.event.get():
                self.keyboard.on_event(event)
                if event.type == pygame.QUIT:
                    print('Average FPS: ', self.clock.get_fps())
                    exit()

            pygame.display.flip()
    
    @classmethod
    def layout_CH():
        return ['1234567890', 'qwertzuiop', 'asdfghjkl', 'yxcvbnm']


def main():
    app = App()
    app.load()


if __name__ == '__main__':
    main()
