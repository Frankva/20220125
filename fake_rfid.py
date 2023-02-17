from time import sleep
import sys

class Rfid:
    '''
    simulate rfid.py to test the script on pc without rfid scanner
    '''
    def read_pipe(self, pipe: dict) -> None:
        '''
        put a fake id in a dict in arg
        '''
        sleep(1)
        #pipe['id_badge'] = 483985410385
        #pipe['id_badge'] = 483985410398
        pipe['id_badge'] = 589402514225 # poma
        #pipe['id_badge'] = 42 # test prénom
        #self.pipe['id_badge'] = 183985410385
        # pipe['id_badge'] = 47 # Trois-Sept Un-Cinq
        # pipe['id_badge'] = 53 # 
        pipe['id_badge'] = 63 # 
        print('fake_badge', file=sys.stderr)