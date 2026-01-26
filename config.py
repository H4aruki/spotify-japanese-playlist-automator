#config.py
#情報の取得
#githubへのアップロード禁止

import os
from dotenv import load_dotenv

#.envファイルの内容を環境変数として読み込む
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8888/callback"   #自身を表す世界共通のアドレス

SCOPE = "user-library-read playlist-read-private playlist-modify-public playlist-modify-private"

Japanese_playlist_id = os.getenv("JAPANESE_PLAYLIST_ID")   #日本語曲専用のプレイリストid
