import pygame

class App:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 480))

    def load(self):
        self.backgrond_color = pygame.Color('#ffffff')
        pygame.mouse.set_visible(False)
        self.mouse = Mouse()
        while True:
            self.event = pygame.event.get()
            for event in self.event:
                if event.type == pygame.QUIT:
                    exit()
            self.update()
            self.draw()

    def update(self):
        #print(pygame.mouse.get_pressed())
      #  print(pygame.mouse.get_pos())
        #print(pygame.MOUSEBUTTONDOWN)
        #print(pygame.MOUSEWHEEL)
        self.mouse.update(self.event)


    def draw(self):
        self.screen.fill(self.backgrond_color)
        pygame.display.flip()


class Mouse:
    def __init__(self) -> None:
        self.left = False
        self.old_left = False

    def update(self, event):
        self.old_left = self.left
        self.left = pygame.mouse.get_pressed()[0] or (pygame.FINGERUP in 
        event)
        print(event)

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