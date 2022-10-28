#!/usr/bin/env python3
import os
import subprocess
import threading
import _thread
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
        self.thread_view = threading.Thread(target=self.view.load)
        #self.log = open("main_log.txt", "a")

        self.rfid = rfid.Rfid()

        self.pipe = dict()
        self.pipe['cancel'] = False
        self.reset_pipe()
        self.model = model.Model()
        self.thread_model_request = None
        self.thread_model_insert = None
        self.thread_model_new_user = None
        self.thread_wait_quit = threading.Thread(target=self.wait_quit,
                args=(self.pipe, ))
        self.thread_send = None
        self.thread_receve = None

    def load(self):
        self.thread_view.start()
        self.thread_wait_quit.start()
        self.view.read_pipe(self.pipe)
        while True:
            self.update()

    def update(self):
        self.do_rfid()
        try:
            self.model.disconnect()
        except:
            pass
        finally:
            self.model.connect()
        self.invoke_receve_logs() # to test if there are more waiting screen
        self.turn_on_screen()
        self.do_model_request()
        print('unknown', self.is_unknown())
        if self.is_unknown():
            self.view.do_unknown_badge_dict(self.pipe)
        else:
            self.view.do_select_scene_dict(self.pipe)

        # check unknown
        self.wait_choice()
        if self.pipe['quit']:
            quit()
        if self.is_cancel():
            self.reset()
            return
        if self.pipe['new_user_valid']:
            self.do_model_new_user()
            self.reset()
            return
        self.invoke_insert()
        self.view.do_wait_scene()
        self.invoke_send_log()
        self.invoke_receve_logs()
        self.reset()
    
    def invoke_insert(self):
        self.safe_wait_thread(self.thread_model_insert)
        self.thread_model_insert = threading.Thread(
            target=self.model.call_insert_log, args=((self.pipe['id_badge'],
                                                      self.pipe['inside']), ))
        self.thread_model_insert.start()
        self.thread_model_insert.join()
    
    def invoke_send_log(self) -> None:
        '''
        manage thread to send all new logs from local
        '''
        print('invoke_send_log')
        self.safe_wait_thread(self.thread_send)
        self.thread_send = threading.Thread(
            target=self.model.send_logs)
        self.thread_send.start()
        self.thread_send.join()

    def invoke_receve_logs(self) -> None:
        '''
        manage thread to receve all new logs from remote
        '''
        print('invoke_receve_logs')
        self.safe_wait_thread(self.thread_receve)
        self.thread_receve = threading.Thread(
            target=self.model.invoke_receive_logs)
        self.thread_receve.start()
        self.thread_receve.join()


    @staticmethod
    def wait_quit(pipe):
        wait_thread = pipe['th_condition']
        wait_thread.acquire()
        while not pipe['quit']:
            wait_thread.wait()
        wait_thread.release()
        print('exit wait_quit')
        _thread.interrupt_main() 


    def is_cancel(self):
        return self.pipe['cancel']

    @staticmethod
    def turn_on_screen():
        try:
            if os.name != 'nt':
                subprocess.run(['xset', 'dpms', 'force', 'on'])
        except:
            pass

    def do_rfid(self):
        '''
        scanne rfid, put id in pipe
        with a thread
        '''
        print('do_rfid()')
        self.thread_rfid = threading.Thread(target=self.rfid.read_pipe,
                                            args=(self.pipe, ))
        self.thread_rfid.start()
        self.thread_rfid.join()

    def do_model_request(self):
        '''
        read user data from database
        with a thread
        '''
        print('do_model_request()')
        self.safe_wait_thread(self.thread_model_request)
        self.thread_model_request = threading.Thread(
            target=self.model.read_name_log, args=(self.pipe, ))
        self.thread_model_request.start()
        self.thread_model_request.join()
        print('end do_model_request', self.pipe)

    def do_model_new_user(self):
        print('do_model_new_user()')
        self.safe_wait_thread(self.thread_model_new_user)
        self.thread_model_new_user = threading.Thread(
            target=self.model.invoke_new_user, args=(self.pipe, ))
        self.thread_model_new_user.start()
        self.thread_model_new_user.join()
    

    def filterInsert(self):
        name = list()
        #name.append('date')
        name.append('id_badge')
        name.append('inside')
        return dict(filter(lambda pipe: pipe[0] in name, self.pipe.items()))

    def safe_wait_thread(self, thread):
        '''
        Wait (block the execution) the end of a thread.
        Check if the thread is running.
        '''
        try:
            if thread.is_alive():
                thread.join()
        except:
            pass

    def wait_choice(self):
        wait_thread = self.pipe['th_condition']
        wait_thread.acquire()
        while ((self.pipe["inside"] == None) and (not self.is_cancel()) and
                (not self.pipe['new_user_valid']) and (not self.pipe['quit'])):
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
        self.pipe['quit'] = False

    def reset(self):
        print('reset()')
        self.reset_pipe()
        #self.model.disconnect()
        #self.model.connect()
        #self.view.do_wait_scene()

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
