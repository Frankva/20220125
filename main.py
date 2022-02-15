
import threading
import view 
from time import sleep

import rfid
import model

class App:
    '''
    controle view script, rfid script, model script
    '''


    def __init__(self):
      
        self.view = view.View
        self.theard_view = threading.Thread(target=self.view)
        self.log = open("main_log.txt", "a")
       
        self.rfid = rfid.Rfid()
       
        self.pipe = dict()

        self.model = model.Model()
        self.tableName = "log"
        
        


    def load(self):
        self.theard_view.start()
        while True:
            self.update()

    def update(self):
        self.theard_rfid = threading.Thread(target=self.rfid.read_pipe, args=(self.pipe, ))
        self.theard_rfid.start()
        self.theard_rfid.join()
        self.do_next_scene()

        self.wait_choice()
        print(self.pipe)
        self.log.write(str(self.pipe))
        
        #self.model.insert(self.tableName, self.create_dict_model())
        try:
            if self.theard_model.is_alive():
                self.theard_model.join()
        except:
            pass

        self.theard_model = threading.Thread(target=self.model.insert, args=(self.tableName, self.pipe))
        self.theard_model.start()
        self.reset()



    def wait_choice(self):
         while self.choice == dict():
            sleep(1)

    def do_next_scene(self):
        '''
        in view
        '''
        self.view.current_scene = "select"
        self.view.pipe = self.choice

    def create_dict_model(self):
        '''
        depreciated
        
        create a dict to give to a sql request
        '''
        d = dict()
        d["id"] = self.id[0]
        d["date"] = "'" + str(self.choice["date"]) + "'"
        d["inside"] = self.choice["inside"]
        return d

    def reset_pipe(self):
        self.pipe = dict()
        
    
    def reset_scene(self):
        self.view.current_scene = "wait"

    def reset(self):
        self.reset_pipe()
        self.reset_scene()



    def __del__(self):
        self.log.close()

def main():
    app = App()
    app.load()


if __name__ == "__main__":
    main()