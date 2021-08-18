import requests
import base64
import json
import pprint

from decouple import config
CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")

initial_uri = input('Copy and paste Spotify Playlist URI here:\n')
print(initial_uri)

plain_uri = initial_uri.split(':')[-1]
print(plain_uri)

url = 'https://accounts.spotify.com/api/token'
headers = {}
data = {}

message = f"{CLIENT_ID}:{CLIENT_SECRET}"
messageBytes = message.encode('ascii')
base64Bytes = base64.b64encode(messageBytes)
base64Message = base64Bytes.decode('ascii')

headers['Authorization'] = f'Basic {base64Message}'
data['grant_type'] = 'client_credentials'

r = requests.post(url, headers = headers, data=data)

token = r.json()['access_token']
pp = pprint.PrettyPrinter(indent=2)
headers = {
            "Authorization": "Bearer " + token,
    }

playlist_url = f'https://api.spotify.com/v1/playlists/{plain_uri}/tracks'

playlist_res = requests.get(url=playlist_url, headers=headers)

playlist_json = json.dumps(playlist_res.json())
this_playlist = json.loads(playlist_json)

pp.pprint(this_playlist)

# for track in this_playlist:
#     song_url = track['external_urls']['href']
#     print(song_url)