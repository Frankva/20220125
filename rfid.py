import sys


import RPi.GPIO
from mfrc522 import SimpleMFRC522 as Reader




class Rfid:
    def __init__(self) -> None:
        self.debug = True
        if self.debug:
            print("Rfid.init", file=sys.stderr)
        self.running = False
        self.reader = Reader()
        self.id = None
        self.text = None

    def __del__(self):
        if self.debug:
            print("Rfid.del", file=sys.stderr)
        RPi.GPIO.cleanup()
    
    def load(self):
        self.read()
       # self.write()
        while self.running:
            self.update()
    
    def update(self):
        if self.debug:
            print("Rfid.update", file=sys.stderr)
        
    def write(self):
        '''
        try to write on a badge with 48… id
        '''
        if self.debug:
            print("Rfid.write", file=sys.stderr)
        if self.id == 483985410385:
            self.reader.write("Ceci est un test d'ecriture")
    
    def read(self) -> int:
        if self.debug:
            print("Rfid.read", file=sys.stderr)
        self.id, self.text = self.reader.read()
        if self.debug:
            print(f"id : {self.id}, typeid :  {type(self.id)}, text : {self.text}")
        return self.id
    
    def read_list(self, result):
        '''
        put id in a list in arg
        '''
        result.append(self.read())
    
    

if __name__ == "__main__":
    rfid = Rfid()
    rfid.load()