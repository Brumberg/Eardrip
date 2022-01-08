
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import logging

class remotedatabase():
    """Remote access handler for spotify queries"""

    #: Doc comment for class attribute Foo.bar.
    #: It can have multiple lines.

    cid = 'b60b806692b04243994cbb6768f91f01'
    secret = 'c07eda245b414bd6b6212ceff40cf681'
    sp = 0

    def __init__(self):
        """constructor - establish connection to spotify webserver with default user key and password and memorize handle

        """
        cid = self.cid
        secret = self.secret
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        self.sp = sp

    def __del__(self):
        """destructuor - release resources

        """
        logging.info("Terminate spotify connection")

    def GetAttributes(self, track=None, artist=None, genre=None):
        """GetAttributes return a list of attributes from the spotify playlist. They are finally being used to optimize
        the recommendation algorithm.

        :param self: list of attributes TBD
        :type name: list or tuple
        :return value: collection of lists of matches

        """

        artist_name = []
        track_name = []
        popularity = []
        track_id = []
        track_uri = []
        sp = self.sp

        #searchfilter = 'track:{track}, artist:{artist}, genre:={genre}'.format(track=track, artist=artist, genre=genre)
        search_filter = ''
        if track != None:
            search_filter = 'track:{track}'.format(track=track)

        if artist != None:
            add_filter = 'artist:{artist}'.format(artist=artist)
            if len(search_filter) > 0:
                search_filter = search_filter + ', ' + add_filter
            else:
                search_filter = add_filter

        if genre != None:
            add_filter = 'genre:={genre}'.format(genre=genre)
            if len(search_filter) > 0:
                search_filter = search_filter + ', ' + add_filter
            else:
                search_filter = add_filter

        for i in range(0, 25, 5):
            track_results = sp.search(q=search_filter, limit=50, offset=i)
            for i, t in enumerate(track_results['tracks']['items']):
                artist_name.append(t['artists'][0]['name'])
                track_name.append(t['name'])
                track_id.append(t['id'])
                popularity.append(t['popularity'])
                track_uri.append(t['uri'])

        return artist_name, track_name, popularity, track_id, track_uri

    def GetTrackAnalytics(self, track_uri=None):
        """GetTrackAnalytics returns a list of attributes associated with the track_uri
        This list encompasses (incomplete listing, see e.g.
        https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features)

        * acousticness
        * danceability
        * energy
        * instrumentalness
        * liveness
        * loudness
        * mode (modality)
        * speechiness
        * tempo
        * time_signature
        * valence



        :param self: list of attributes TBD
        :type name: list or tuple
        :return value: collection of lists of matches

        """
        features = []
        if len(track_uri)>100:
            track_uri = track_uri[0:100]

        try:
            features = self.sp.audio_features(track_uri)
        except:
            print('Execution failed')

        return features
