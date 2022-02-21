import threading
import time

class A:
    def __init__(self):
        self.n = True
        while self.n:
            time.sleep(2)
    def end(self):
        self.n = False


th = threading.Thread(target=A)
th.run()
input()
