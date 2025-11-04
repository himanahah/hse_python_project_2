import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import logging

# Настройка базового логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='script.log',
    filemode='w'
)

load_dotenv()
logging.info("Загружены переменные из .env")

client_id = os.getenv('client_id_sp')
client_secret = os.getenv('client_secret_sp')
redirect_uri = os.getenv('redirect_uri_sp')

try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri
    ))
    logging.info("Аутентификация успешно выполнена")
except Exception as e:
    logging.error(f"Ошибка при аутентификации: {e}")
    raise

playlist_id = '0Hm1tCeFv45CJkNeIAtrfF'

try:
    logging.info(f"Получение данных о треках из плейлиста: {playlist_id}")
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    logging.info(f"Получено треков: {len(tracks)}")
except Exception as e:
    logging.error(f"Ошибка запроса к плейлисту: {e}")
    raise

artists = []

for item in tracks:
    track = item['track']
    artist_name = track['artists'][0]['name']
    artists.append(artist_name)
    logging.info(f"Артист: {artist_name}")

print(artists)
