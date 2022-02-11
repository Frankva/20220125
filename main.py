import os
import threading
import view 
from time import sleep

#import rfid

class App:
    '''
    controle view script, rfid script, model script
    '''
    rasp = os.name != "nt"

    def __init__(self):
            
        self.view = view.View
        self.theard_view = threading.Thread(target=self.view)
        self.log = open("main_log.txt", "a")
        if self.rasp:
            self.rfid = rfid.Rfid()
            self.id = list()
            self.theard_rfid = threading.Thread(target=self.rfid.read_list, args=(self.id, ))
            self.choice = dict()

    def load(self):
        self.theard_view.start()
        if self.rasp:
            self.theard_rfid.start()
            self.theard_rfid.join()
            print(self.id)
            self.log.write(self.id)
        self.view.do_next_scene_dict(self.choice)
        while self.choice == dict():
            sleep(1)
        self.log.write(self.choice)
        #self.view.current_scene = "select"
    
    def __del__(self):
        self.log.close()

def main():
    app = App()
    app.load()


if __name__ == "__main__":
    main()