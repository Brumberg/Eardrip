
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

    def GetArtistInfo(self, artist_uri):
        """GetArtistInfo returns additional information like the genre

        :param self: list of attributes TBD
        :type name: list or tuple
        :return value: collection of lists of matches

        """
        artist_info_list = []
        for i in artist_uri:
            artist_info_list.append(self.sp.artist(i))
        return artist_info_list

    def GetAttributes(self, track=None, artist=None, genre=None, max_no_tracks=10, packet_size=5):
        """GetAttributes return a list of attributes from the spotify playlist. They are finally being used to optimize
        the recommendation algorithm.

        :param self: list of attributes TBD
        :type name: list or tuple
        :return value: collection of lists of matches

        """

        track_properties = list()
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

        for i in range(0, max_no_tracks, packet_size):
            track_results = sp.search(q=search_filter, limit=packet_size, offset=i)
            if track_results == None:
                break

            for i, t in enumerate(track_results['tracks']['items']):
                property_concatenation = dict()
                property_concatenation['artist'] = t['artists'][0]['name']
                property_concatenation['artist_uri'] = t['artists'][0]['external_urls']['spotify']
                property_concatenation['track'] = t['name']
                property_concatenation['track_id'] = t['id']
                property_concatenation['popularity'] = float(t['popularity'])
                property_concatenation['uri'] = t['uri']
                track_properties.append(property_concatenation)

        return track_properties

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
            logging.error('Execution failed')

        return features