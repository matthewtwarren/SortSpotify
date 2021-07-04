"""A playlist class."""
from .playlist import Playlist
from .user_account import UserAccount

class PlaylistLibrary:
    """A class used to represent a playlist created by the user."""

    def __init__(self):
        self._all_playlists = {}

    def create_playlist(self):
        """Creates a new playlist"""

        playlist_name = input("Enter a name for your playlist: ")
        self._all_playlists[playlist_name] = Playlist(playlist_name)
        print(f"Playlist {playlist_name} created.\n")

    def show_playlists(self):
        """Shows all the playlists created this session"""

        if (len(self._all_playlists) == 0):
            print("You have not created any playlists yet."
            "To create a playlist type: create playlist.")
        else:
            for playlist in self._all_playlists:
                print(playlist)
        print()

    def select_playlist(self,function):
        """Selects the playlist based on user input or automatically if there is only one playlist in the library.

        Args:
            function: Purpose of selecting the playlist e.g "filter". Used in printed instructions.
        """
        if (len(self._all_playlists) == 0):
            print("You have not created any playlists yet."
            "To add tracks to a playlist, first create a playlist by typing: create playlist.")
            return
        elif (len(self._all_playlists) == 1):
            return next(iter(self._all_playlists.values()))
        else:
            print(f"Enter the name of the playlist you would like to {function}: \n")
            for playlist in self._all_playlists:
                print(f"   {playlist}")
            print()
            selected_playlist = input()
            return self._all_playlists[selected_playlist]

    def add_to_playlist(self,user_account):
        """Adds tracks to a user playlist"""

        selected_playlist = self.select_playlist("add to")
        if selected_playlist is None:
            pass
        else:
            selected_playlist.add_playlist(user_account)

    def filter_playlist(self, user_account):
        """Filter tracks in a playlist"""

        playlist_selection = self.select_playlist("filter")
        if len(playlist_selection._tracks) > 0:
            feature_selection = input("How would you like to filter the playlist (by tempo or key)?: ")
            if feature_selection.lower() == "tempo":
                filter_selection = input("Please enter a BPM range (e.g. 110:120): ")
                filter_formatted = [*map(float,filter_selection.split(":"))]
                playlist_selection.filter_tracks_by_tempo(filter_formatted, user_account)
            elif feature_selection.lower() == "key":
                filter_selection = input("Please enter the keys using Camelot notation (e.g. 11B,12B,12A): ")
                filter_formatted = [key for key in filter_selection.split(",")]
                playlist_selection.filter_tracks_by_key(filter_formatted, user_account)
            else:
                print("Please enter a valid selection. Tracks can only be filtered by tempo or key\n.")
        else:
            print("Your playlist is empty. Add to the playlist before filtering.\n")
            return
