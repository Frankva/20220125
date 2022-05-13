import threading
import view
try:
    import rfid
except:
    import fake_rfid as rfid
import model


class App:
    '''
    controle view script, rfid script, model script
    '''

    def __init__(self):
        self.view = view.View()
        self.theard_view = threading.Thread(target=self.view.load)
        #self.log = open("main_log.txt", "a")

        self.rfid = rfid.Rfid()

        self.pipe = dict()
        self.pipe['cancel'] = False
        self.reset_pipe()
        self.model = model.Model()
        self.tableName = "log"
        self.theard_model_request = None
        self.theard_model_insert = None
        self.theard_model_new_user = None

    def load(self):
        self.theard_view.start()
        while True:
            self.update()

    def update(self):
        self.do_rfid()
        #self.do_next_scene()
        self.do_model_request()
        print('unknown', self.is_unknown())
        if self.is_unknown():
            self.view.do_unknown_badge_dict(self.pipe)
        else:
            self.view.do_select_scene_dict(self.pipe)

#        print(self.pipe)
        # check unknown
        self.wait_choice()
        if self.is_cancel():
            self.reset()
            return
        if self.pipe['new_user_valid']:
            self.do_model_new_user()
            self.reset()
            return
        #self.log.write(str(self.pipe))
        #self.model.insert(self.tableName, self.create_dict_model())
        self.safe_wait_thread(self.theard_model_insert)
        self.theard_model_insert = threading.Thread(target=self.model.insert,
                                args=(self.tableName, self.filterInsert()))
        self.theard_model_insert.start()
        self.theard_model_insert.join()
        self.reset()



    def is_cancel(self):
        return self.pipe['cancel']

    def do_rfid(self):
        '''
        scanne rfid, put id in pipe
        with a thread
        '''
        print('do_rfid()')
        self.theard_rfid = threading.Thread(target=self.rfid.read_pipe,
                                            args=(self.pipe, ))
        self.theard_rfid.start()
        self.theard_rfid.join()

    def do_model_request(self):
        '''
        read user data from database
        with a thread
        '''
        print('do_model_request()')
        self.safe_wait_thread(self.theard_model_request)
        self.theard_model_request = threading.Thread(
            target=self.model.read_name_log, args=(self.pipe, ))
        self.theard_model_request.start()
        self.theard_model_request.join()
        print('end do_model_request', self.pipe)

    def do_model_new_user(self):
        print('do_model_new_user()')
        self.safe_wait_thread(self.theard_model_new_user)
        self.theard_model_new_user = threading.Thread(
            target=self.model.invoke_new_user, args=(self.pipe, ))
        self.theard_model_new_user.start()
        self.theard_model_new_user.join()
    

    def filterInsert(self):
        name = list()
        name.append('date')
        name.append('id_badge')
        name.append('inside')
        return dict(filter(lambda pipe: pipe[0] in name, self.pipe.items()))

    def safe_wait_thread(self, thread):
        try:
            if thread.is_alive():
                thread.join()
        except:
            pass

    def wait_choice(self):
        wait_thread = self.pipe['th_condition']
        wait_thread.acquire()
        while (self.pipe["inside"] == None) and \
                (not self.is_cancel()) and (not self.pipe['new_user_valid']):
            wait_thread.wait()
            print('choice done')
            wait_thread.release()

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
        self.pipe = dict()
#        self.pipe["id"] = None
#        self.pipe["date"] = None
        self.pipe["inside"] = None
        self.pipe["log"] = list()
        self.pipe["name"] = ''
        self.pipe["surname"] = ''
        self.pipe['id_badge'] = None
        self.pipe['cancel'] = False
        self.pipe['new_user_valid'] = False
        self.pipe['th_condition'] = threading.Condition()

    def reset(self):
        print('reset()')
        self.reset_pipe()
        self.model.disconnect()
        self.model.connect()
        self.view.do_wait_scene()

    def __del__(self):
        pass
        #self.log.close()

#    def fake_rfid(self):
#        '''
#        to test the script when no rfid scanner
#        '''
#        print('fake_rfid()')
#        sleep(10)
#        #self.pipe['id_badge'] = 483985410385
#        self.pipe['id_badge'] = 183985410385
#
    def is_unknown(self):
        print('name', self.pipe['name'])
        return self.pipe['name'] == ''



def main():
    app = App()
    app.load()



if __name__ == "__main__":
    main()
