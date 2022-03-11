
import threading
import view
from time import sleep

#import rfid
import model


class App:
    '''
    controle view script, rfid script, model script
    '''

    def __init__(self, is_rfid=True):
        self.is_rfid = is_rfid
        self.view = view.View()
        self.theard_view = threading.Thread(target=self.view.load)
        self.log = open("main_log.txt", "a")


        if self.is_rfid:
            self.rfid = rfid.Rfid()


        self.pipe = dict()
        self.reset_pipe()
        self.model = model.Model()
        self.tableName = "log"
        self.theard_model_request = None
        self.theard_model_insert = None

    def load(self):
        self.theard_view.start()
        while True:
            self.update()

    def update(self):
        self.do_rfid()
        print(self.pipe)
        self.do_next_scene()
        self.do_model_request()
        self.wait_choice()
        print(self.pipe)
        self.log.write(str(self.pipe))

        #self.model.insert(self.tableName, self.create_dict_model())
        self.safe_wait_thread(self.theard_model_insert)
        print('before insert')
        print(self.filterInsert())

        self.theard_model_insert = threading.Thread(
            target=self.model.insert, args=(self.tableName, self.filterInsert()))
        self.theard_model_insert.start()
        self.reset()

    def do_rfid(self):
        print('do_rfid()')
        if self.is_rfid:
            self.theard_rfid = threading.Thread( target=self.rfid.read_pipe, args=(self.pipe, ))
            self.theard_rfid.start()
            self.theard_rfid.join()
        else:
            self.fake_rfid()
    
    def do_model_request(self):
        print('do_model_request()')
        self.safe_wait_thread(self.theard_model_request)
        self.theard_model_request = threading.Thread(target=self.model.read_name_log, args=(self.pipe, ))
        self.theard_model_request.start()
        self.theard_model_request.join()

    def filterInsert(self):
        name = list()
        name.append('date')
        name.append('id_badge')
        name.append('inside')
        return dict(filter( lambda pipe: pipe[0] in name, self.pipe.items()))

    def safe_wait_thread(self, thread):
        try:
            if thread.is_alive():
                thread.join()
        except:
            pass

    def wait_choice(self):
        while self.pipe["inside"] == None:
            print("wait_choice")
            sleep(1)

    def do_next_scene(self):
        '''
        in view
        '''
        self.view.current_scene = "select"
        self.view.pipe = self.pipe
    

#    def create_dict_model(self):
#        '''
#        depreciated
#     
#        create a dict to give to a sql request
#        '''
#        d = dict()
#        d["id"] = self.id[0]
#        d["date"] = "'" + str(self.choice["date"]) + "'"
#        d["inside"] = self.choice["inside"]
#        return d

    def reset_pipe(self):
        self.pipe["id"] = None
        self.pipe["date"] = None
        self.pipe["inside"] = None
        self.pipe["name"] = ''
        self.pipe["surname"] = ''
        self.pipe['id_badge'] = None

    def reset_scene(self):
        self.view.current_scene = "wait"
        print(self.view.current_scene)

    def reset(self):
        print('reset()')
        self.reset_pipe()
        self.reset_scene()

    def __del__(self):
        self.log.close()
    
    def fake_rfid(self):
        '''
        to test the script when no rfid scanner
        '''
        print('fake_rfid()')
        sleep(10)
        self.pipe['id_badge'] = 483985410385
    



def main():
    app = App()
    app.load()

def test1():
    app = App(False)
    app.load()

if __name__ == "__main__":
    mode = 1
    if mode == 0:
        main()
    elif mode == 1:
        test1()
