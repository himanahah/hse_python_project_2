import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
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

client_id = os.getenv('SPOTIPY_CLIENT_ID') or os.getenv('client_id_sp')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET') or os.getenv('client_secret_sp')

if not client_id or not client_secret:
    logging.error("Отсутствуют client_id или client_secret. Установите SPOTIPY_CLIENT_ID и SPOTIPY_CLIENT_SECRET или client_id_sp/client_secret_sp в .env")
    raise RuntimeError("No client_id or client_secret.")

try:
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    logging.info("Аутентификация (Client Credentials) успешно выполнена")
except Exception as e:
    logging.error(f"Ошибка при аутентификации (Client Credentials): {e}")
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
