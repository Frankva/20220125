import sys
from time import sleep
import RPi.GPIO
from mfrc522 import SimpleMFRC522 as Reader

class App:
    def __init__(self) -> None:
        self.debug = True
        if self.debug:
            print("App.init", file=sys.stderr)
        self.running = True
        self.reader = Reader()

    def __del__(self):
        if self.debug:
            print("App.del", file=sys.stderr)
        RPi.GPIO.cleanup()
    def main(self):
        while self.running:
            self.update()
    def update(self):
        if self.debug:
            print("App.update", file=sys.stderr)
        id, text = self.reader.read()
        print(f"id : {id}, text : {text}")
        sleep(5)

def main():
    app = App()
    app.main()

if __name__ == "__main__":
    main()