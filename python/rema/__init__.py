
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

    def GetAttributes(self, track):
        """GetAttributes return a list of attributes from the spotify playlist. They are finally being used to optimize the recommendation algorithm.

        :param self: list of attributes TBD
        :type name: list or tuple
        :return value: collection of lists of matches

        """

        artist_name = []
        track_name = []
        popularity = []
        track_id = []
        sp = self.sp
        searchfilter = 'track:{track}'.format(track=track)
        for i in range(0, 25, 5):
            track_results = sp.search(q=searchfilter, type='track', limit=50, offset=i)
            for i, t in enumerate(track_results['tracks']['items']):
                artist_name.append(t['artists'][0]['name'])
                track_name.append(t['name'])
                track_id.append(t['id'])
                popularity.append(t['popularity'])
        return artist_name, track_name, popularity, track_id
