import sys
import spotipy
import spotipy.util as util

''' shows the albums and tracks for a given artist.
'''

def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None

def show_artist_albums(artist):
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    seen = set() # to avoid dups
    albums.sort(key=lambda album:album['name'].lower())
    for album in albums:
        name = album['name']
        if name not in seen:
            print((' ' + name))
            seen.add(name)

if __name__ == '__main__':
    scope = 'user-library-read'

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print "Usage: %s username" % (sys.argv[0],)
        sys.exit()

    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)

        tracks = sp.album_tracks('44aVVevMGKS4q6nWXbELpP')
        for track in tracks['items']:
            print track['name']
            features = sp.audio_features(str(track['id']))
            print features[0]['energy']
            #recommendations = sp.recommendations(str(track['id']))
            #print recommendations
        if len(sys.argv) < 2:
            print 'Usage: {0} artist name'.format(sys.argv[0])
        else:
            name = ' '.join(sys.argv[1:])
            artist = get_artist(name)
            if artist:
                show_artist_albums(artist)
            else:
                print("Can't find that artist")