import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_spotify_artists():
    # URL страницы — используем хост без www, чтобы избежать ошибки сертификата
    url = 'https://kworb.net/spotify/artists.html'
    
    # Заголовки для имитации браузера
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    
    try:
        # Получаем страницу (попытка с проверкой сертификата)
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
        except requests.exceptions.SSLError:
            # fallback: отключаем проверку сертификата (временное решение, небезопасно)
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.get(url, headers=headers, verify=False, timeout=15)
            response.raise_for_status()
        
        # Парсим HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Находим таблицу
        table = soup.find('table')
        
        # Списки для данных
        artists_data = []
        
        # Проходим по всем строкам таблицы (пропускаем заголовок)
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) >= 5:  # Проверяем, что в строке достаточно столбцов
                artist_info = {
                    'Rank': cols[0].text.strip(),
                    'Artist': cols[1].text.strip(),
                    'Daily Streams': cols[2].text.strip(),
                    'Peak Daily': cols[3].text.strip(),
                    'Monthly Listeners': cols[4].text.strip()
                }
                artists_data.append(artist_info)
        
        # Создаем DataFrame
        df = pd.DataFrame(artists_data)
        
        # Сохраняем в CSV
        df.to_csv('spotify_artists.csv', index=False)
        print(f"Данные успешно собраны и сохранены в spotify_artists.csv")
        return df
        
    except requests.RequestException as e:
        print(f"Ошибка при получении данных: {e}")
        return None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None

if __name__ == "__main__":
    # Добавляем задержку для вежливого скрапинга
    time.sleep(2)
    df = scrape_spotify_artists()
    if df is not None:
        print("\nПервые 5 строк данных:")
        print(df.head())