import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import pprint
import pandas as pd

client_id = ''
client_secret = ''
artist_id = '2lP3N5eROnUo5QucxqAp8c'

client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

artist = '1XYuC1vxinTjHCNd5clB8C'

#アルバム情報を取得する。Spotify APIの仕様上、最新50アルバムまで。
#全部出したければプレイリスト作って補完するしかない
#2019/11/9現在でピカンチまで 
results = spotify.artist_albums(artist, album_type='single', country='JP', limit=50, offset=0)

artist_albums = []
for song in results['items'][:len(results['items'])]:
    data = [
        song['name'], 
        song['id']]
    artist_albums.append(data)

#アルバムからトラック情報を取得する
song_info_track = []
for artist_album in artist_albums:
    album_id = artist_album[1]
    song_info = spotify.album_tracks(album_id, limit=50, offset=0)

    #両A面があるのでトラックを抜き出す
    for song_info_detail in song_info['items'][:len(song_info)]:
        song_track_id = song_info_detail['id']
        song_title = song_info_detail['name']
        #曲の情報を抜き出す
        result = spotify.audio_features(song_track_id)
        
        #なぜか取得できない曲があったので（取得したIDで検索できない）、分岐をする
        if result[0] is not None:
            #タイトルを入れた辞書を作成
            result[0]['title'] = song_title
            pd.DataFrame(result)
            song_info_track.append(result[0])
        
df = pd.io.json.json_normalize(song_info_track)
df = df.set_index('title')
#見やすくするため不要な列を削除する
#今回はID情報などを削除する。 インストでもないのでinstrumentalnessも削除する
df = df.drop(['type', 'id', 'uri', 'track_href','analysis_url', 'time_signature', 'mode','instrumentalness'], axis=1)
df
