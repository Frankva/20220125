from urllib.request import urlopen
from urllib.parse import quote
import hmac
import json
import urllib.error

class APIClient:
    def __init__(self) -> None:
        self.base_url = 'https://timbreuse.sectioninformatique.net/Logs'
        self.method = ('add', 'get_logs')

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
        return f'{quote(str(date))}/{badge_id}/{inside}/{token}'
    
    @staticmethod
    def create_url(base_url, method, arg) -> str:
        return f'{base_url}/{method}/{arg}'

    def send(self, url) -> tuple:
        '''
        wrap function of urllib.request.urlopen
        '''
        print('send')
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
        
    
    def send_log(self, date, badge_id, inside):
        arg = self.create_arg(date, badge_id, inside, self.create_token(
            date, badge_id, inside)
        )
        url = self.create_url(self.base_url, self.method[0], arg)
        tmp = self.send(url)
        print(type(tmp))
        print(tmp)
        return tmp[1]

    def receve_logs(self, log_id) -> list[dict]:
        '''
        receve all logs from the server
        '''
        print('receve_logs')
        print(log_id)
        url = self.create_url(self.base_url, self.method[1], log_id)
        print(url)
        html_file = self.send(url)[0]
        return json.loads(html_file.readline())

    

def fake_info_stamping() -> tuple:
    import datetime
    date = datetime.datetime.now()
    badge_id = 42
    inside = 1
    inside = 1 if bool(inside) else 0
    return date, badge_id, inside

def main():
    test = 2
    if test == 0:
        pass
    if test == 1:
        client_API = APIClient()
        client_API.invoke_send_log(*fake_info_stamping())
    if test == 2:
        client_API = APIClient()
        tmp = client_API.receve_logs(413)
        print(type(tmp), tmp)
        print(type(tmp[0]), tmp[0])


if __name__ == "__main__":
    main()
