import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import clientID, clientSecret
import requests 

client_credentials_manager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def getPlaylistSongs(link):
    uris,names,durations,explicits,tracknumbers = [],[],[],[],[]
    # playlist = sp.playlist_items(link)
    playlist = sp.playlist_tracks(link)
    for item in playlist['items']:
        # print(item['track']['name'],item['track']['uri'],item['track']['duration_ms'],item['track']['explicit'],item['track']['track_number'])
        uris.append(item['track']['uri'])
        names.append(item['track']['name'])
        durations.append(item['track']['duration_ms'])
        explicits.append(item['track']['explicit'])
        tracknumbers.append(item['track']['track_number'])

    songsDF = pd.DataFrame({
        'uri':uris,
        'name':names,
        'duration':durations,
        'explicit':explicits,
        'tracknumber':tracknumbers,
    })

    return songsDF

def getSongFeatures(songsDF):
    danceability, energy, key, loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo = [], [], [], [], [], [], [], [], [], []

    for song in songsDF['uri']:
        features = sp.audio_features(song)[0]
        danceability.append(features['danceability'])
        energy.append(features['energy'])
        key.append(features['key'])
        loudness.append(features['loudness'])
        speechiness.append(features['speechiness'])
        acousticness.append(features['acousticness'])
        instrumentalness.append(features['instrumentalness'])
        liveness.append(features['liveness'])
        valence.append(features['valence'])
        tempo.append(features['tempo'])
    
    featuresDF = pd.DataFrame({
        'danceability': danceability,
        'energy': energy,
        'key': key,
        'loudness': loudness,
        'speechiness': speechiness,
        'acousticness': acousticness,
        'instrumentalness': instrumentalness,
        'liveness': liveness,
        'valence': valence,
        'tempo': tempo
    })

    return featuresDF

def combineDFs(songsDF, featuresDF):
    fullDetailsDF = songsDF.merge(featuresDF,left_index = True, right_index = True)

    # print(fullDetailsDF.head())
    avgFeatures = fullDetailsDF.describe().loc['mean']
    print(fullDetailsDF.describe().loc['mean'])

    return avgFeatures

def fullAnalysis():
    links = [{'name':'Good Estrogen','url':'https://open.spotify.com/playlist/4Hwk9UNYLxemqaLuByw5Gm?si=e54b0ab4ab4d4f6e'}, 
    {'name': 'Workout','url':'https://open.spotify.com/playlist/5oKUsLqwBG601zOWt7cAp4?si=3a310fef8a984132'},
    {'name': 'Alternative Rock Playlist','url':'https://open.spotify.com/playlist/0wAj7pTSzEsVsmsSCYu2X7?si=0a8f5f0ee71f498d'}, 
    {'name': 'Rap Playlist','url':'https://open.spotify.com/playlist/6DzkdXwp4sR3vg5zpoQUk5?si=9c2d284969dc45b0'},
    {'name': 'Party Playlist','url':'https://open.spotify.com/playlist/5YJ83niMY5fNjQNQPnj2YH?si=f93174fd444f4e3b'}]

    allPlaylistsDF = pd.DataFrame(columns=[
        'danceability',
        'energy',
        'key',
        'loudness',
        'speechiness',
        'acousticness',
        'instrumentalness',
        'liveness',
        'valence',
        'tempo'
    ])

    for link in links:
        songsDF = getPlaylistSongs(link['url'])
        featuresDF = getSongFeatures(songsDF)
        avgFeatures = combineDFs(songsDF, featuresDF)   

        allPlaylistsDF = allPlaylistsDF.append([avgFeatures]) 
    
    playlistName = ['Good Estrogen','Workout','Alternative Rock Playlist','Rap Playlist', 'Party Playlist']

    allPlaylistsDF.insert(0,"Playlist Name", playlistName,True)

    # allPlaylistsDF.to_csv('output.csv')
    print(allPlaylistsDF)

fullAnalysis()