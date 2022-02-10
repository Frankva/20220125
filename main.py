import os
import threading
import view 

import os

class App:
    '''
    controle view script, rfid script, model script
    '''
    rasp = os.name != "nt"
    if rasp:
        import rfid
        print("raspberry")

    def __init__(self):
            
        self.view = view.View
        self.theard_view = threading.Thread(target=self.view)
        if self.rasp:
            self.rfid = rfid.Rfid()
            self.id = list()
            self.theard_rfid = threading.Thread(target=self.rfid.read_list, args=(self.id))

    def load(self):
        self.theard_view.start()
        if self.rasp:
            self.theard_rfid.start()
            self.theard_rfid.join()
        
        input()
        self.view.current_scene = "select"


def main():
    app = App()
    app.load()


if __name__ == "__main__":
    main()