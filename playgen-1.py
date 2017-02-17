import sys
import spotipy
import spotipy.util as util
import random
from scipy import stats

def eval(playlist):
    ''' Evaluation function for a single playlist. Playlist energies are divided into equal
    halves and a linear regression is performed on each half. Returns a value which is
    largest in the case of a tight fit (large abs(R values)) and an increasing
    trend in energy for the first half and decreasing trend for the second half (slope1 -
    slope2). 
    '''
    index = len(playlist) // 2
    i1, i2, l1, l2 = ([] for i in range(4))
    idx = 0
    for track in playlist:
        energy = track[1]
        if idx < index:
            i1.append(idx)
            l1.append(energy)
        else:
            i2.append(idx)
            l2.append(energy)
        idx += 1
    slope1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(i1, l1)
    slope2, intercept2, r_value2, p_value2, std_err2 = stats.linregress(i1, l2)
    return slope1 * abs(r_value1) - slope2 * abs(r_value2)

def generate_population(playlists, num_playlists):
    ''' Create the next generation of playlist objects by randomly pairing
    from the list of playlists and performing crossovers. If new playlists are
    evaluated to be better than old playlists, replace the old playlists in the list.
    '''
    indices = list(range(num_playlists))
    random.shuffle(indices)
    index = 0
    while index < num_playlists - 1:
        p1 = playlists[indices[index]]
        p2 = playlists[indices[index + 1]]
        r1, r2 = crossover(p1, p2)
        if eval(p1) + eval(p2) < eval(r1) + eval(r2):
            playlists[indices[index]] = r1
            playlists[indices[index + 1]] = r2
        index += 2

def crossover(p1, p2):
    ''' Perform single-point crossover on two playlists to generate two new playlists.
    '''
    s = min(len(p1), len(p2))
    index = random.randint(0, s)
    new_p1 = []
    new_p2 = []
    for i in range(0, index):
        new_p1.append(p1[i])
        new_p2.append(p2[i])
    for i in range(index, s):
        new_p1.append(p2[i])
        new_p2.append(p1[i])
    return new_p1, new_p2

if __name__ == '__main__':
    population_size = 50
    num_generations = 200
    playlists = []
    scope = 'playlist-modify-public'

    if len(sys.argv) == 4:
        username = sys.argv[1]
        playlist_name = sys.argv[2]
        track_id = sys.argv[3]
    else:
        print "Usage: %s username playlist_name track_id" % (sys.argv[0],)
        sys.exit()

    token = util.prompt_for_user_token(username, scope, 'e4c540c6ba7844b5abb3daee8c30d791',
    '8f8b4095e9394038a0082f2035a99842', 'http://127.0.0.1')

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False

        new_playlist = sp.user_playlist_create(username, playlist_name)
        
        trackList = []
        trackList.append(track_id)
        print "Loading initial playlists..."
        for i in range(0, population_size):
            playlist = []
            recommendations = sp.recommendations(seed_tracks = trackList, limit = 10) #10-song playlists
            for track in recommendations['tracks']:
                features = sp.audio_features(str(track['id']))
                playlist.append((track, features[0]['energy']))
            playlists.append(playlist)
        print "Created initial playlists"
        for i in range(0, num_generations):
            print i
            generate_population(playlists, population_size)
        '''for ps in playlists:
            for tup in ps:
                print tup[0]['name'], tup[1]
            print '\n' '''
        maxEval = 0
        maxPlaylist = []
        for ps in playlists:
            newEval = eval(ps)
            if newEval > maxEval:
                maxEval = newEval
                maxPlaylist = ps
        for tup in maxPlaylist:
            print tup[0]['name'], tup[1]
            sp.user_playlist_add_tracks(username, new_playlist['id'], [tup[0]['id']])
        print '\n'
