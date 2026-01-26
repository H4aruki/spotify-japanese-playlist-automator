
from spotify_client import SpotifyClient
from song_judgement import is_japanese_song
import config
import time

# 実行時のログを 'app.log' というファイルに保存する設定
# 'a' は追記モードなので、実行するたびに履歴が積み重なります
import sys
sys.stdout = open('app.log', 'a', encoding='utf-8')
sys.stderr = open('error.log', 'a', encoding='utf-8') # エラー専用のログ


def origin():
    print("処理を開始します...")
    client = SpotifyClient()   #Spotifyクライアントを初期化
    
    # お気に入り曲のIDを取得（既存の関数を使用）
    track_ids = client.get_track_ids_from_liked_playlist()
    print(f"お気に入りの曲数：{len(track_ids)}")
    
    # 日本語曲を判定してプレイリストに追加
    # 各track IDからtrackオブジェクトを取得して日本語判定
    uris_to_add = []
    processed_count = 0
    
    for track_id in track_ids:
        # track IDからtrackオブジェクトを取得
        track_info = client.sp.track(track_id)
        if is_japanese_song(track_info, client):
            print(f"日本語曲を追加: {track_info['name']} by {track_info['artists'][0]['name']}")
            uris_to_add.append(track_info['uri'])
        
        processed_count += 1
        print(f"処理済み: {processed_count}/{len(track_ids)}")
        
        # API制限を避けるために0.5秒待機
        time.sleep(0.5)
    
    # プレイリストに追加（100曲ずつ分割）
    if uris_to_add:
        print(f"日本語曲を{len(uris_to_add)}曲追加します。")
        for i in range(0, len(uris_to_add), 100):
            chunk = uris_to_add[i:i+100]
            client.add_tracks_to_playlist(config.Japanese_playlist_id, chunk)
            # プレイリスト追加後も少し待機
            time.sleep(1)
    else:
        print("日本語曲はありません。")
    
    print("処理が完了しました。")


def main():
    print("処理を開始します...")
    client = SpotifyClient()   #Spotifyクライアントを初期化
    existig_ids = client.get_ids_from_playlist(config.Japanese_playlist_id)   #日本語プレイリストの既存曲IDを取得
    print(f"既存の曲数：{len(existig_ids)}")

    liked_songs = client.get_latest_liked_songs(limit=50)   #最新のお気に入り曲50曲を取得

    #新規曲の抽出と判定
    uris_to_add = []
    for item in liked_songs:
        track = item['track']
        if track['id'] not in existig_ids:
            if is_japanese_song(track, client):
                print(f"日本語曲を追加: {track['name']} by {track['artists'][0]['name']}")
                uris_to_add.append(track['uri'])

    #プレイリストに追加
    if uris_to_add:
        print(f"新規日本語曲を{len(uris_to_add)}曲追加します。")
        client.add_tracks_to_playlist(config.Japanese_playlist_id, uris_to_add)
    else:
        print("新規日本語曲はありません。")
    
    print("処理が完了しました。")


"""
#まずこちらを実行。
if __name__ == "__main__":
    
    origin()
"""



#続いてこちらを実行。origin()の部分はコメントアウト。
if __name__ == "__main__":
    main()

