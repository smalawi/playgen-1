import sys
import spotipy
import spotipy.util as util

''' shows the albums and tracks for a given artist.
'''

#if __name__ == '__main__':
scope = 'playlist-modify-public'

if len(sys.argv) == 4:
    username = sys.argv[1]
    print username
    playlist_id = sys.argv[2]
    album_id = sys.argv[3]
else:
    print "Usage: %s username playlist_id album_id" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)

    tracks = sp.album_tracks(album_id)
    ordered = []
    for track in tracks['items']:
        features = sp.audio_features(str(track['id']))
        energy = features[0]['energy']
        if len(ordered) == 0:
            ordered.append((str(track['id']), energy))
        else:
            for i in range(0, len(ordered)):
                if ordered[i][1] < energy:
                    ordered.insert(i, (str(track['id']), energy))
                    break
    track_ids = [track[0] for track in ordered]
    sp.user_playlist_add_tracks(username, playlist_id, track_ids)

        #recommendations = sp.recommendations(str(track['id']))
        #print recommendations