from time import sleep

class Rfid:
    '''
    simulate rfid.py to test the script on pc without rfid scanner
    '''
    def read_pipe(self, pipe: dict) -> None:
        '''
        put a fake id in a dict in arg
        '''
        sleep(3)
        #pipe['id_badge'] = 483985410385
        pipe['id_badge'] = 483985410395
        #self.pipe['id_badge'] = 183985410385