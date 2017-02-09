import sys
import spotipy
import spotipy.util as util
import random


def splice(p1, p2):
    s = min(len(p1), len(p2))
    index = random.randint(0, s)
    new_p1 = []
    new_p2 = []
    for i in range(0, index):
        new_p1[i] = p1[i]
        new_p2[i] = p2[i]
    for i in range(index, s):
        new_p1[i] = p2[i]
        new_p2[i] = p1[i]
    return new_p1, new_p2
    
if __name__ == '__main__':
    scope = 'playlist-modify-public'

    if len(sys.argv) == 4:
        username = sys.argv[1]
        playlist_id = sys.argv[2]
        album_id = sys.argv[3]
    else:
        print "Usage: %s username playlist_id album_id" % (sys.argv[0],)
        sys.exit()

    token = util.prompt_for_user_token(username, scope, 'e4c540c6ba7844b5abb3daee8c30d791',
    '8f8b4095e9394038a0082f2035a99842', 'http://127.0.0.1')

    if token:
        sp = spotipy.Spotify(auth=token)

        tracks = sp.album_tracks(album_id)
        trackList = []
        for track in tracks['items']:
            trackList.append(track['id'])
            recommendations = sp.recommendations(seed_tracks = trackList, limit = 5)
            for tracko in recommendations['tracks']:
                print tracko['name'], tracko['artists'][0]['name']
            trackList.pop()
            print '\n'
        #print recommendations
        #for track in recommendations['tracks']:
            print track['name'], track['artists'][0]['name']
    
        '''tracks = sp.album_tracks(album_id)
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
        sp.user_playlist_add_tracks(username, playlist_id, track_ids)'''

            #recommendations = sp.recommendations(str(track['id']))
            #print recommendations