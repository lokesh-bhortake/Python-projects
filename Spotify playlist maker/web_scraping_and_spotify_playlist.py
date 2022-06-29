from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy import SpotifyOAuth
import pprint

dt = input("Of which day you want your songs to be? Type date in format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{dt}/")

html = response.text
soup = BeautifulSoup(html, "html.parser")

songs = [h3.getText().replace("\n", "") for h3 in soup.findAll("h3", class_="a-no-trucate")]


SPOTIPY_CLIENT_ID = 'YOUR_CLIENT_ID_HERE'
SPOTIPY_CLIENT_SECRET = 'YOUR_SPOTIPY_CLIENT_SECRET_HERE'
SPOTIPY_REDIRECT_URI = 'https://example.com/'
scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"))

user = sp.current_user()["id"]
pp = pprint.PrettyPrinter(indent=2)

# Searching Spotify for songs by title
song_uris = []
for song in songs:
    result = sp.search(q=f'track:{song} year:{dt[:4]}', type='track')
    pp.pprint(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user, name=f"{dt} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

