from urllib.request import urlopen
from urllib.parse import quote
import hmac
import json
import urllib.error
from functools import reduce
import sys
import warnings
from enum import Enum

class Method(Enum):
    ADD = 'add'
    GET_LOGS = 'get_logs'
    GET = 'get'
class Controller(Enum):
    LOGS = 'Logs'
    BADGES = 'Badges'

class APIClient:
    def __init__(self) -> None:
        self.base_url = 'https://timbreuse.sectioninformatique.net'
        # self.controller = ('Logs', 'Badges')
        # self.method = ('add', 'get_logs')

    @staticmethod
    def load_key() -> str:
        with open('.key.json', 'r') as file:
            return json.load(file)['key']

    def create_token(self, date, badge_id, inside) -> str:
        text = f'{date}{badge_id}{inside}'.encode()
        key = self.load_key().encode()
        token_text = hmac.new(key, text, 'sha256').hexdigest()
        return token_text

    @staticmethod
    def create_arg(date, badge_id, inside, token) -> str:
        warnings.warn("use create_arg_args", DeprecationWarning)
        return f'{quote(str(date))}/{badge_id}/{inside}/{token}'
    
    @staticmethod
    def create_url(base_url, method, arg) -> str:
        warnings.warn("use create_url_n", DeprecationWarning)
        return f'{base_url}/{method}/{arg}'

    def create_url_n(self, controller:str, method:str, arg:str) -> str:
        '''
        >>> api_client = APIClient()
        >>> api_client.create_url_n('Logs', 'add', '2/3/4')
        'https://timbreuse.sectioninformatique.net/Logs/add/2/3/4'
        '''
        # return f'{base_url}/{method}/{arg}'
        return (f'{self.base_url}/{controller}/'
        f'{method}/{arg}')

    def send(self, url) -> tuple:
        '''
        wrap function of urllib.request.urlopen
        '''
        print('send', file=sys.stderr)
        try:
            html_file = urlopen(url)
        #    # print(html_file.read())
        #    # print()
        #    # print(html_file.url)
        #    # print(html_file.status)
        #    # print(html_file.headers)
        #    # return html_file
            return html_file, html_file.status
        except urllib.error.HTTPError as e:
            return None, str(e)
        
    
    def send_log(self, date, badge_id, inside) -> tuple:
        '''
        >>> client_API = APIClient()
        >>> file, code = client_API.send_log(*fake_info_stamping())
        >>> type(file)
        <class 'http.client.HTTPResponse'>
        >>> code
        201
        '''
        print('APIClient.send_log', file=sys.stderr)
        arg = self.create_arg_args(date, badge_id, inside, self.create_token(
            date, badge_id, inside)
        )
        url = self.create_url_n(Controller.LOGS.value, Method.ADD.value, arg)
        return self.send(url)

    def receive_logs(self, log_id) -> list[dict]:
        '''
        receive all logs from the server
        >>> api_client = APIClient()
        >>> logs = api_client.receive_logs(413)
        >>> type(logs)
        <class 'list'>
        >>> type(logs[0])
        <class 'dict'>
        '''
        print('receive_logs', file=sys.stderr)
        print(log_id, file=sys.stderr)
        url = self.create_url_n(Controller.LOGS.value, Method.GET_LOGS.value, 
            log_id)
        print(url, file=sys.stderr)
        html_file = self.send(url)[0]
        
        return json.loads(html_file.readline())

    def send_badge_and_user(self, badge_id:int, name:str, surname:str):
        '''
        >>> api_client = APIClient()
        >>> file, code = api_client.send_badge_and_user(44, 'John', 'Malc')
        >>> type(file)
        <class 'http.client.HTTPResponse'>
        >>> code
        201
        '''
        print('APIClient.send_badge_and_user', file=sys.stderr)
        arg = self.create_arg_args(badge_id, name, surname,
            self.create_token_args(badge_id, name, surname))
        url = self.create_url_n(Controller.BADGES.value, Method.ADD.value, arg)
        print(url, file=sys.stderr)
        return self.send(url)

    def receive_users_and_badges(self, badge_id) -> list[dict]:
        '''
        receive all users and badges from the server
         >>> api_client = APIClient()
         >>> logs = api_client.receive_users_and_badges(97)
         >>> type(logs)
         <class 'list'>
         >>> type(logs[0])
         <class 'dict'>
        '''
        print('receive_users_and_badges', file=sys.stderr)
        print(badge_id, file=sys.stderr)
        url = self.create_url_n(Controller.BADGES.value, Method.GET.value,
            badge_id)
        print(url, file=sys.stderr)
        html_file = self.send(url)[0]
        return json.loads(html_file.readline())

    @staticmethod
    def create_arg_args(*args) -> str:
        '''
        >>> APIClient.create_arg_args('a', 'b', 'c')
        'a/b/c'
        '''
        print('create_arg_args', file=sys.stderr)
        text = reduce(lambda cumulator, word:f'{cumulator}/{word}', args)
        return quote(text)

    def create_token_args(self, *args) -> str:
        '''
        >>> badge_id, name, surname = 1, 'Sam', 'Smith'
        >>> api_client = APIClient()
        >>> api_client.create_token_args(badge_id, name, surname)
        'c8261428a992984fea981d45714c09c3f0207423e0f1626c2508ae171aa4c134'
        '''
        text = reduce(lambda cumulator, word:f'{cumulator}{word}',
            args).encode()
        key = self.load_key().encode()
        token_text = hmac.new(key, text, 'sha256').hexdigest()
        return token_text
    

def fake_info_stamping() -> tuple:
    import datetime
    date = datetime.datetime.now()
    badge_id = 42
    inside = 1
    inside = 1 if bool(inside) else 0
    return date, badge_id, inside

def main():
    test = 0
    if test == 0:
        import doctest
        doctest.testmod()
    elif test == 1:
        pass

if __name__ == "__main__":
    main()
