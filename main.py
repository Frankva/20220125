#!/usr/bin/env python
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
import sys
import warnings


class App:
    '''
    controle view script, rfid script, model script
    '''

    def __init__(self):
        self.HAS_REMOTE_SERVER = True
        self.suspend_screen_time = 10*60
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
        self.thread_send_log = None
        self.thread_send_badges_and_users = None
        self.thread_receive_log = None
        # self.thread_receive_users_and_badges = None
        self.thread_receive_users = None
        self.thread_receive_badges = None

    def load(self):
        self.turn_off_screen_interval(self.suspend_screen_time)
        self.thread_view.start()
        self.thread_wait_quit.start()
        self.view.read_pipe(self.pipe)
        while True:
            self.update()

    def update(self):
        if self.HAS_REMOTE_SERVER:
            self.synchronize_user_badge_log_with_remote()
        self.do_rfid()
        self.reconnect_local_db()
        if self.HAS_REMOTE_SERVER:
            self.synchronize_user_badge_log_with_remote()
        self.turn_on_screen()
        self.do_model_request()
        print('unknown', self.is_unknown(), file=sys.stderr)
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
            # self.invoke_send_unsync_badges_and_users()
            self.reset()
            return
        self.invoke_insert()
        self.view.do_wait_scene()
        # self.invoke_send_log()
        # self.invoke_receive_logs()
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
        print('invoke_send_log', file=sys.stderr)
        self.safe_wait_thread(self.thread_send_log)
        self.thread_send_log = threading.Thread(
            target=self.model.send_logs)
        self.thread_send_log.start()
        self.thread_send_log.join()
    
    def invoke_send_unsync_badges_and_users(self) -> None:
        '''
        manage thread to send all new badges and users
        '''
        print('invoke_send_unsync_badges_and_users', file=sys.stderr)
        self.safe_wait_thread(self.thread_send_badges_and_users)
        self.thread_send_badges_and_users = threading.Thread(
            target=self.model.send_unsync_badges_and_users)
        self.thread_send_badges_and_users.start()
        self.thread_send_badges_and_users.join()


    def invoke_receive_logs(self) -> None:
        '''
        manage thread to receive all new logs from remote
        '''
        print('invoke_receive_logs', file=sys.stderr)
        self.safe_wait_thread(self.thread_receive_log)
        self.thread_receive_log = threading.Thread(
            target=self.model.invoke_receive_logs)
        self.thread_receive_log.start()
        self.thread_receive_log.join()

    def invoke_receive_users_and_badges(self) -> None:
        '''
        Deprecation
        manage thread to receive all users and badges
        '''
        print('invoke_receive_users_and_badges', file=sys.stderr)
        warnings.warn("use create_arg_args", DeprecationWarning)
        self.safe_wait_thread(self.thread_receive_users_and_badges)
        self.thread_receive_users_and_badges = threading.Thread(
            target=self.model.invoke_receive_users_and_badges)
        self.thread_receive_users_and_badges.start()
        self.thread_receive_users_and_badges.join()

    def invoke_join_thread(self, thread:str, function, args=()):
        '''
        manage thread in procedural way
        '''
        print('invoke_join_thread', 'thread', thread, 'function', function,
              file=sys.stderr)
        self.safe_wait_thread(getattr(self, thread))
        setattr(self, thread, threading.Thread(target=function, args=args))
        print('before start invoke_join_thread', 'thread', thread, 'function',
              function, file=sys.stderr)
        getattr(self, thread).start()
        print('before join invoke_join_thread', 'thread', thread, 'function',
              function, file=sys.stderr)
        getattr(self, thread).join()
        print('end invoke_join_thread', 'thread', thread, 'function', function,
              file=sys.stderr)



    @staticmethod
    def wait_quit(pipe):
        wait_thread = pipe['th_condition']
        wait_thread.acquire()
        while not pipe['quit']:
            wait_thread.wait()
        wait_thread.release()
        print('exit wait_quit', file=sys.stderr)
        _thread.interrupt_main() 


    def is_cancel(self):
        return self.pipe['cancel']

    @staticmethod
    def turn_on_screen() -> None:
        try:
            # do it only on the Raspberry Pi
            if os.name != 'nt':
                subprocess.run(['xset', 'dpms', 'force', 'on'])
                # subprocess.run(['xset', 'dpms', 'force', 'on', 's', '60s'])
                # subprocess.run(['xset', 'dpms', 'fp', 'default'])
                # subprocess.run(['xset', 'dpms', 'force', 'off', 's', '30s'])
        except Exception:
            pass

    @staticmethod
    def turn_off_screen_interval(interval: int) -> None:
        '''
        turn off screen after inactivity times
        Parameters:
            interval(int): interval in second off
        '''
        try:
            # do it only on the Raspberry Pi
            if os.name != 'nt':
                # subprocess.run(['xset', 'dpms', 'force', 'standby', 's',
                #                 str(interval) + 's'])

                subprocess.run(['xset', 's', str(interval) + 's'])
        except Exception:
            pass

    def do_rfid(self):
        '''
        scanne rfid, put id in pipe
        with a thread
        '''
        print('do_rfid()', file=sys.stderr)
        self.thread_rfid = threading.Thread(target=self.rfid.read_pipe,
                                            args=(self.pipe, ))
        self.thread_rfid.start()
        self.thread_rfid.join()

    def do_model_request(self):
        '''
        read user data from database
        with a thread
        '''
        print('do_model_request()', file=sys.stderr)
        self.invoke_join_thread('thread_model_request', 
                                self.model.find_user_info, args=(self.pipe, ))
        # self.safe_wait_thread(self.thread_model_request)
        # self.thread_model_request = threading.Thread(
        #     target=self.model.read_name_log, args=(self.pipe, ))
        # self.thread_model_request.start()
        # self.thread_model_request.join()
        print('end do_model_request', self.pipe, file=sys.stderr)

    def do_model_new_user(self):
        print('do_model_new_user()', file=sys.stderr)
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
            print('choice done', file=sys.stderr)
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
        print('reset()', file=sys.stderr)
        self.reset_pipe()
        #self.model.disconnect()
        #self.model.connect()
        #self.view.do_wait_scene()

    def __del__(self):
        pass
        #self.log.close()


    def is_unknown(self):
        print('name', self.pipe['name'], file=sys.stderr)
        return self.pipe['name'] == ''

    def synchronize_user_badge_log_with_remote(self):
        print('synchronize_user_badge_log_with_remote', file=sys.stderr)
        self.invoke_send_unsync_badges_and_users()
        self.invoke_send_log()
        self.invoke_join_thread('thread_receive_users',
                                self.model.invoke_receive_users)
        self.invoke_join_thread('thread_receive_badges',
                                self.model.invoke_receive_badges)
        self.invoke_receive_logs() 

    def reconnect_local_db(self):
        try:
            self.model.disconnect()
        except:
            pass
        finally:
            self.model.connect()


def main():
    app = App()
    app.load()

def doctest():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    if False:
        doctest()
        exit()

    main()
