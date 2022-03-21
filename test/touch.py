import pygame

class App:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 480))

    def load(self):
        self.backgrond_color = pygame.Color('#ffffff')
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            self.update()
            self.draw()

    def update(self):
        print(pygame.mouse.get_pressed())

    def draw(self):
        self.screen.fill(self.backgrond_color)
        pygame.display.flip()


class Mouse:
    def __init__(self) -> None:
        self.left = False
        self.old_left = False

    def update(self):
        self.old_left = self.left
        self.left = pygame.mouse.get_pressed()[0]

    def release(self, button: str):
        '''
        detect release click
        up click
        
        '''
        return (not getattr(self, button)) and (getattr(self, f"old_{button}"))

def main():
    app = App()
    app.load()

if __name__ == '__main__':
    main()