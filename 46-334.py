import logging
import os
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def get_chart(datestr: str):
    chart_url = URL + datestr

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    try:
        resp = requests.get(url=chart_url, headers=headers)
        resp.raise_for_status()
        logging.info(f'Response received')
        return resp.text
    except requests.exceptions.RequestException as req_err:
        logging.warning(f'Request Error: {req_err} | {resp.url} | {resp.headers}')
    except Exception as err:
        logging.error(f'Unexpected Error: {err}')
    return None


class SpotifyService:
    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.sp = self.spotify_auth()

    def spotify_auth(self):
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope="playlist-modify-private",
                redirect_uri="http://127.0.0.1:8000/spotify/redirect",
                client_id=self.client_id,
                client_secret=self.client_secret,
                show_dialog=True,
                cache_path="token.txt",
                username='irfan'
            )
        )

        return sp

    def get_songs(self, year: str, songs_in_chart: list[str]):
        song_uri = []

        for song in songs_in_chart:
            result = self.sp.search(q=f'track: {song} year: {year}', type='track')
            # logging.info(result)

            try:
                uri = result.get('tracks').get('items')[0].get('uri')
                song_uri.append(uri)
            except IndexError:
                logging.warning(f'{song} does not exist. Skipping...')

        return song_uri

    def create_playlist(self, date: str, song_uris: list):
        user_id = self.sp.current_user().get('id')

        playlist = self.sp.user_playlist_create(user=user_id, name=f'{date} Billboard 10', public=False)

        self.sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)

        logging.info('Playlist added')


def main():
    today = (datetime.now() - timedelta(days=DAY_FROM_CUR)).strftime('%Y-%m-%d')
    resp = get_chart(today)

    if resp:
        resp_soup = BeautifulSoup(resp, 'html.parser')
        song_name_spans = resp_soup.select("li ul li h3")
        song_names = [song.text.strip() for song in song_name_spans[:10]]

        i_spotify = SpotifyService()
        songs_uri = i_spotify.get_songs(today.split('-')[0], song_names)
        i_spotify.create_playlist(today, songs_uri)
    else:
        logging.warning(f'Response was empty')


if __name__ == '__main__':
    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

    URL = "https://www.billboard.com/charts/hot-100/"
    DAY_FROM_CUR = 1
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

    main()
