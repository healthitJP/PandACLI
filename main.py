#!/usr/bin/env python3
import argparse
import sys
from panda_client import PandAClient

def main():
    parser = argparse.ArgumentParser(description='PandAにログインしてCookieを取得するCLIツール')
    parser.add_argument('username', help='PandAのユーザー名')
    parser.add_argument('password', help='PandAのパスワード')
    
    args = parser.parse_args()
    
    try:
        # PandAClientのインスタンスを作成
        client = PandAClient()
        
        # ユーザー情報をセット
        client.set_user(args.username, args.password)
        
        # ログイン
        client.login()
        
        # Cookieを取得して表示
        cookie_str = '; '.join([f"{cookie.name}={cookie.value}" for cookie in client.cookies])
        print(cookie_str)
        
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 