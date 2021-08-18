import requests
import base64
import json
import pprint
import csv


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

playlist_url = f'https://api.spotify.com/v1/playlists/{plain_uri}/tracks?market=US'

playlist_res = requests.get(url=playlist_url, headers=headers)

playlist_json = json.dumps(playlist_res.json())
this_playlist = json.loads(playlist_json)

tracks = this_playlist['items']
pp.pprint(tracks)
print('-------Song URLs Here---------')

song_array = []
for track in tracks:
    song_href = track['track']['href']
    song_url = f'{song_href}?market=US'
    song_res = requests.get(url=song_url, headers=headers)
    song_json = json.dumps(song_res.json())
    this_song = json.loads(song_json)
    pp.pprint(this_song)
    artist_href = this_song['artists'][0]['href']
    artist_url = f'{artist_href}?market=US'
    artist_res = requests.get(url=artist_url, headers=headers)
    artist_json = json.dumps(artist_res.json())
    this_artist = json.loads(artist_json)
    song_artist = {**this_song, **this_artist}
    song_array.append(song_artist)

songs = {'songs': song_array}
with open('data.json', 'a') as outfile:
    json.dump(songs, outfile)

with open('data.json') as json_file:
    data = json.load(json_file)

song_data = data['songs']

data_file = open('data_file.csv', 'w')

csv_writer = csv.writer(data_file)

count = 0

for song in song_data:
    if count == 0:
        header = song.keys()
        csv_writer.writerow(header)
        count+=1
    
    csv_writer.writerow(song.values())

    data_file.close()
