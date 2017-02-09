import sys
import spotipy
import spotipy.util as util

''' shows the albums and tracks for a given artist.
'''

#if __name__ == '__main__':
scope = 'playlist-modify-public'

if len(sys.argv) == 3:
    username = sys.argv[1]
    album_id = sys.argv[2]
else:
    print "Usage: %s username album_id" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope, 'e4c540c6ba7844b5abb3daee8c30d791',
'8f8b4095e9394038a0082f2035a99842', 'http://127.0.0.1')

if token:
    sp = spotipy.Spotify(auth=token)

    tracks = sp.album_tracks(album_id)
    print "Acousticness:"
    for track in tracks['items']:
        features = sp.audio_features(str(track['id']))
        print features[0]['acousticness']
    print '\n', "Danceability:"
    for track in tracks['items']:
        features = sp.audio_features(str(track['id']))
        print features[0]['danceability']
    print '\n', "Energy:"
    for track in tracks['items']:
        features = sp.audio_features(str(track['id']))
        print features[0]['energy']
    print '\n', "Tempo:"
    for track in tracks['items']:
        features = sp.audio_features(str(track['id']))
        print features[0]['tempo']
    print '\n', "Valence:"
    for track in tracks['items']:
        features = sp.audio_features(str(track['id']))
        print features[0]['valence']