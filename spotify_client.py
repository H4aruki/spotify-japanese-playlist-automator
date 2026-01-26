
#API関連の処理モジュール

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import config



class SpotifyClient:
    def __init__(self):

        auth_manager = SpotifyOAuth(client_id = config.CLIENT_ID, client_secret = config.CLIENT_SECRET, redirect_uri = config.REDIRECT_URI, scope = config.SCOPE)
        sp = spotipy.Spotify(auth_manager=auth_manager)

        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        self.artist_cache = {} # アーティスト情報のキャッシュ

        
    #お気に入りプレイリストの曲IDを取得
    def get_track_ids_from_liked_playlist(self) -> set:
        result = self.sp.current_user_saved_tracks()
        tracks = result['items']   #itemsは１曲の情報のすべてを取得するためのもの

        track_ids = set()
        while result['next']:
            result = self.sp.next(result)   # sp.next()で次のページのデータを取得
            tracks.extend(result['items'])

        for item in tracks:
            track_ids.add(item['track']['id'])

        return track_ids

    #指定されたプレイリストの全曲IDを取得
    def get_ids_from_playlist(self, playlist_id):
        ids = []
    # 最初の100曲を取得
        results = self.sp.playlist_items(playlist_id)
    
        while results:
            # 現在のページにある曲のIDをリストに集める
            for item in results['items']:
                # 楽曲データが正常に存在する場合のみIDを取得
                if item['track'] and item['track']['id']:
                    ids.append(item['track']['id'])
        
            # 次の100曲（nextページ）があるかチェック
            if results['next']:
                # 次のページを取得してresultsを更新
                results = self.sp.next(results)
            else:
                # 次のページがなければループ終了
                break
            
        return ids
    
    def get_latest_liked_songs(self, limit: int = 50) -> list:
        result = self.sp.current_user_saved_tracks(limit=limit)
        return result['items']

    def get_artist_genres(self, artist_id: str) -> list:
        artist_info = self.sp.artist(artist_id)
        return artist_info['genres']

    def add_tracks_to_playlist(self, playlist_id: str, track_ids: list):
        for i in range(0, len(track_ids), 50):
            chunk = track_ids[i:i+50]
            self.sp.playlist_add_items(playlist_id, chunk)







#get_track_ids_from_liked_playlist()のテスト
#print(len(SpotifyClient().get_track_ids_from_liked_playlist()))

#print(SpotifyClient().get_track_ids_from_liked_playlist())