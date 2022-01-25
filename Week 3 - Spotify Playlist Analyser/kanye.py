import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import clientID, clientSecret
import requests 
import plotly.express as px
import plotly.graph_objects as go


client_credentials_manager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def getPlaylistSongs(link):
    uris,names= [],[]
    album = sp.album_tracks(link)
    for item in album['items']:
        uris.append(item['uri'])
        names.append(item['name'])

    songsDF = pd.DataFrame({
        'uri':uris,
        'name':names,
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
        'speechiness': speechiness,
        'acousticness': acousticness,
        'instrumentalness': instrumentalness,
        'valence': valence,
    })

    return featuresDF

def combineDFs(songsDF, featuresDF):
    fullDetailsDF = songsDF.merge(featuresDF,left_index = True, right_index = True)
    avgFeatures = fullDetailsDF.describe().loc['mean']
    print(fullDetailsDF.describe().loc['mean'])

    return avgFeatures

def fullAnalysis():
    links = [{'name':'The College Dropout','url':'https://open.spotify.com/album/4Uv86qWpGTxf7fU7lG5X6F?si=x2jASa9TSpGEYUpr0iCyZA'},
        {'name':'Late Registration','url':'https://open.spotify.com/album/5ll74bqtkcXlKE7wwkMq4g?si=bRJa4IsASJ2kl2F25wlKFA'},
        {'name':'808s & Heartbreaks','url':'https://open.spotify.com/album/3WFTGIO6E3Xh4paEOBY9OU?si=mkzNXD-YSXCvCYCuLhWX6A'},
        {'name':'Graduation','url':'https://open.spotify.com/album/0TkH5xirnI8LCHYusFZT5X?si=pTP6nGaXSqiUu9gXBYAYNw'},
        {'name':'My Beautiful Dark Twisted Fantasy','url':'https://open.spotify.com/album/20r762YmB5HeofjMCiPMLv?si=_72UORqoQSixaKVNGgd92Q'},
        {'name':'Watch the Throne','url':'https://open.spotify.com/album/7mCeLbChyegbRwwKK5shJs?si=SDsEl0ssQKimzr_jb2V4GQ'},
        {'name':'Yeezus','url':'https://open.spotify.com/album/7D2NdGvBHIavgLhmcwhluK?si=OFHCdfXSR3WVE6TSYUZJxw'},
        {'name':'The Life of Pablo','url':'https://open.spotify.com/album/7gsWAHLeT0w7es6FofOXk1?si=n0-F0B5OS0Crx8hi35Tt4w'},
        {'name':'Ye','url':'https://open.spotify.com/album/2Ek1q2haOnxVqhvVKqMvJe?si=vfPEcFXDS1u5PRIL9br0yw'}, 
        {'name':'Jesus is King','url':'https://open.spotify.com/album/0FgZKfoU2Br5sHOfvZKTI9?si=nrWHSa17QwS1tPcnmwKmvQ'},
        {'name':'Donda','url':'https://open.spotify.com/album/5CnpZV3q5BcESefcB3WJmz?si=3E-xst8pSDulZoEaeJv8rQ'},
    ]

    playlistName = []
    for link in links:
        playlistName.append(link['name'])

    allPlaylistsDF = pd.DataFrame(columns=[
        'danceability',
        'energy',
        'speechiness',
        'acousticness',
        'instrumentalness',
        'valence',
    ])

    for link in links:
        songsDF = getPlaylistSongs(link['url'])
        featuresDF = getSongFeatures(songsDF)
        avgFeatures = combineDFs(songsDF, featuresDF)   

        allPlaylistsDF = allPlaylistsDF.append([avgFeatures]) 
    

    allPlaylistsDF.insert(0,"Playlist Name", playlistName,True)
    print(allPlaylistsDF)


    cat = ['danceability',
        'energy',
        'speechiness',
        'acousticness',
        'instrumentalness',
        'valence']

    fig = go.Figure()
    for index,row in allPlaylistsDF.iterrows():
        fig.add_trace(go.Scatter(
            x = cat, 
            name = row['Playlist Name'],
            y = [row['danceability'],row['energy'],row['speechiness'],row['acousticness'],row['instrumentalness'],row['valence']]
        ))

    fig.update_layout(
    showlegend=True
    )
    fig.show()

    fig2 = go.Figure()
    for index, col in allPlaylistsDF.iloc[:,1:].iteritems():
        print(index)
        fig2.add_trace(go.Scatter(
            x = playlistName, 
            name = index,
            y = col
        ))

    fig2.update_layout(
    showlegend=True
    )
    fig2.show()
    fig.show()
    fig.write_html("kanye_line_graph_by_category.html")
    fig2.write_html("kanye_line_graph_by_album.html")
    print('Done Analysis.')

fullAnalysis()