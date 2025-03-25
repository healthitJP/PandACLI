from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup

@dataclass
class User:
    username: str
    password: str

class PandAClient:
    BASE_URL = "https://panda.ecs.kyoto-u.ac.jp"
    LOGIN_URL = f"{BASE_URL}/cas/login?service=https%3A%2F%2Fpanda.ecs.kyoto-u.ac.jp%2Fsakai-login-tool%2Fcontainer"
    
    def __init__(self):
        self.__logged_in = False
        self.__user = None
        self.__session = requests.session()
    
    def set_user(self, username: str, password: str) -> None:
        self.__user = User(username=username, password=password)
    
    def login(self) -> None:
        if not self.__logged_in:
            try:
                username = self.__user.username
                password = self.__user.password
            except AttributeError:
                raise ValueError("ユーザー情報が設定されていません")
            
            # ログインページを取得してトークンを抽出
            response = self.__session.get(self.LOGIN_URL)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 必要なトークンを取得
            lt = soup.select("#fm1 > div.row.btn-row > input[type=hidden]:nth-of-type(1)")[0].attrs["value"]
            execution = soup.select("#fm1 > div.row.btn-row > input[type=hidden]:nth-of-type(2)")[0].attrs["value"]
            
            # ログインリクエストを送信
            self.__session.post(
                url=self.LOGIN_URL,
                data={
                    "username": username,
                    "password": password,
                    "lt": lt,
                    "execution": execution,
                    "_eventId": "submit",
                },
            )
            self.__logged_in = True
    
    @property
    def cookies(self):
        """現在のセッションのCookieを取得"""
        return self.__session.cookies 