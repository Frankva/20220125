from urllib.request import urlopen
from urllib.parse import quote
import urllib.error
import hmac
import json

class APIClient:
    def __init__(self) -> None:
        self.base_url = 'https://timbreuse.sectioninformatique.net/Logs'
        self.method = 'add'

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

    def send(self, url):
        print('send')
        try:
            #html_file = urlopen(url)
            # print(html_file.read())
            # print()
            # print(html_file.url)
            # print(html_file.status)
            # print(html_file.headers)
            # return html_file
            return urlopen(url).status
        except urllib.error.HTTPError as e:
            return e
    
    def invoke_send_log(self, date, badge_id, inside) -> bool:
        print('invoke_send_log')
        arg = self.create_arg(date, badge_id, inside, self.create_token(
            date, badge_id, inside)
        )
        url = self.create_url(self.base_url, self.method, arg)
        return self.send(url)

def fake_info_stamping() -> tuple:
    import datetime
    date = datetime.datetime.now()
    badge_id = 42
    inside = 1
    inside = 1 if bool(inside) else 0
    return date, badge_id, inside

def main():
    test = 1
    # match test:
    #     case 0:
    #         pass
    #     case 1:
    #         client_API = APIClient()
    #         client_API.invoke_send_log(*fake_info_stamping())


if __name__ == "__main__":
    main()
