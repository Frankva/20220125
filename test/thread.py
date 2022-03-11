import sys
import threading
from time import sleep

class A:
    def __init__(self) -> None:
        self.__pa = 0
        self.running = True

    @property
    def pa(self):
        return self.__pa

    @pa.setter
    def pa(self, a):
        print('setter', self.__pa, a, file=sys.stderr)
        self.__pa = a + 1
    def add2(self):
        print('add2', self.__pa, file=sys.stderr)
        self.__pa += 2
        print('add2 end', self.__pa, file=sys.stderr)
    
    def load(self):
        while self.running:
            self.update()

    def update(self):
            sleep(5)

def main():
    thread_a = threading.Thread(target=A)
    thread_a.start()
    thread_a.pa = 2
    print(thread_a.pa)
    getattr(thread_a, 'add2')()
    print(thread_a.pa)

def test1():
    a = A()
    thread_a = threading.Thread(target=a.load)
    thread_a.start()
    a.pa = 4
    print(a.pa)
    a.add2()
    print(a.pa)



if __name__ == '__main__':
    test1()