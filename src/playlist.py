"""A playlist class."""
from .user_account import UserAccount

class Playlist:
    """A class used to represent a playlist created by the user."""
    def __init__(self, playlist_name):
        self._tracks = []
        self._name = playlist_name

    def add_playlist(self, user_account):
        """Adds tracks from another playlist in the users library to this playlist."""

        print()
        print("Your Spotify playlists:\n")
        user_playlists = self.get_spotify_playlists(user_account, print_switch=True)
        user_selection = input("Enter the number(s) of the playlists to be added (e.g. 0,1,3) or ALL: ")
        if user_selection.lower() == "all":
            index_selection = list(range(len(user_playlists)))
        else:
            index_selection = [int(x)-1 for x in user_selection.split(",")]
        for idx, playlist_name in enumerate(user_playlists):
            if idx in index_selection:
                self.add_tracks(user_account, user_playlists[playlist_name])
                print(f"Tracks from {playlist_name} added to {self._name}")
        print()

    def add_tracks(self, user_account, playlist_id):
        """Adds tracks (track IDs) to playlist class.

        Args:
            user_account: UserAccount class object for accessing Spotify data.
            playlist_id: ID for Spotify playlist containing tracks to be added.
        """

        index = 0
        start_index = 0
        end_index = 99
        while end_index == 99:
            track_batch = user_account._auth_sp.playlist_tracks(playlist_id, offset=start_index, limit=100)
            for index, track in enumerate(track_batch['items']):
                if track['track']['id'] not in self._tracks:
                    self._tracks.append(track['track']['id'])
            end_index = index
            start_index = start_index+100

    def filter_tracks_by_tempo(self, filter, user_account):
        """Filters tracks in the playlist based on their tempo (BPM).

        Args:
            filter: A list containing min and max BPM values for filtering.
            user_account: UserAccount class object for accessing Spotify data.
        """
        filtered_tracks = []
        for track in self._tracks:
            tempo = user_account._auth_sp.audio_features([track])[0]['tempo']
            if tempo >= filter[0] and tempo < filter[1]:
                filtered_tracks.append(track)

        if len(filtered_tracks) == 0:
            print("No tracks in this playlist matched your criteria. Playlist has not been filtered.\n")
        else:
            self._tracks = filtered_tracks
            print(f"Tracks filtered by tempo. Playlist now contains {len(filtered_tracks)} tracks.\n")

    def filter_tracks_by_key(self, filter, user_account):
        """Filters tracks in the playlist based on their tempo (BPM).

        Args:
            filter: A list containing the keys for filtering in Camelot notation.
            user_account: UserAccount class object for accessing Spotify data.
        """
        filtered_tracks = []
        for track in self._tracks:
            spotify_key = user_account._auth_sp.audio_features([track])[0]['key']
            camelot_key = convert_key(spotify_key)
            if camelot_key in filter:
                filtered_tracks.append(track)

        if len(filtered_tracks) == 0:
            print("No tracks in this playlist matched your criteria. Playlist has not been filtered.\n")
        else:
            self._tracks = filtered_tracks
            print(f"Tracks filtered by key. Playlist now contains {len(filtered_tracks)} tracks.\n")

    def sort_tracks_by_tempo(self, user_account, ascending_order):
        """Sort the tracks in the playlist based on their tempo.

        Args:
            user_account: UserAccount class object for accessing Spotify data.
            ascending_order: Whether the tracks should be sorted in ascending (T) or descending (F) order.
        """
        track_tempos = []
        for track in self._tracks:
            track_tempos.append(user_account._auth_sp.audio_features([track])[0]['tempo'])
        sorted_tracks = [track for _, track in sorted(zip(track_tempos, self._tracks))]
        if ascending_order:
            self._tracks = sorted_tracks
            print("Tracks sorted in ascending order by tempo (BPM).\n")
        else:
            self._tracks = sorted_tracks.reverse()
            print("Tracks sorted in descending order by tempo (BPM).\n")

    def add_to_spotify(self,user_account):
        """Adds the playlist to the users Spotify account.

        Args:
            user_account: UserAccount class object for accessing Spotify data.
        """
        user_account._auth_sp.user_playlist_create(
            user = user_account._username,
            name = self._name,
            public = False,
            collaborative = False,
            description = 'Made using SpotifyDJ and Spotipy.'
            )
        user_spotify_playlists = self.get_spotify_playlists(user_account, print_switch=False)
        playlist_id = user_spotify_playlists[self._name]
        if len(self._tracks) > 100:
            batches = [self._tracks[x:x+100] for x in range(0, len(self._tracks), 100)]
            for batch in batches:
                user_account._auth_sp.playlist_add_items(playlist_id,batch,position=None)
        else:
            user_account._auth_sp.playlist_add_items(playlist_id,self._tracks,position=None)
        print("Playlist added to your Spotify library.\n")

    def convert_key(self, spotify_key):
        """Convert Spotify key notation to Camelot notation

        Args:
            key: Spotify key value (str)
        """
        key_dict = {
            '0,1':'8B',
            '1,1':'3B',
            '2,1':'10B',
            '3,1':'5B',
            '4,1':'12B',
            '5,1':'7B',
            '6,1':'2B',
            '7,1':'9B',
            '8,1':'4B',
            '9,1':'11B',
            '10,1':'6B',
            '11,1':'1B',
            '0,0':'5A',
            '1,0':'12A',
            '2,0':'7A',
            '3,0':'2A',
            '4,0':'9A',
            '5,0':'4A',
            '6,0':'11A',
            '7,0':'6A',
            '8,0':'1A',
            '9,0':'8A',
            '10,0':'3A',
            '11,0':'10A'}

        camelot_key = key_dict[spotify_key]
        return camelot_key

    def get_spotify_playlists(self, user_account, print_switch):
        """Retrieve all playlists in users Spotify library.

        Args:
            user_account: UserAccount class object for accessing Spotify data.
            print_switch: Whether to print the playlist names (boolean)
        """
        user_playlists = {}
        start_index = 0
        end_index = 49
        counter = 0
        while end_index == 49:
            playlist_batch = user_account._auth_sp.user_playlists(
                user_account._username,
                offset = start_index,
                limit = 50)
            for index, playlist in enumerate(playlist_batch['items']):
                counter = counter+1
                user_playlists[playlist['name']] = playlist['id']
                if print_switch:
                    print("{0:4d}  {1}".format(counter,playlist['name']))
            end_index = index
            start_index = start_index+50
        print()

        return(user_playlists)
