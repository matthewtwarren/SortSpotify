"""A command parser class to recieve and execute instructions via the command line"""

from .playlist_library import PlaylistLibrary
from .user_account import UserAccount

class CommandException(Exception):
    pass

class CommandParser:
    """A class to parse and execute user commands"""

    def __init__(self, playlist_library, user_account):
        self._library = playlist_library
        self._account = user_account

    def execute_command(self, command):
        """Executes user command"""

        if not command:
            raise commandException("Please enter a valid command. "
            "Type HELP for a list of available commands.")

        elif command.lower() == "help":
            self.help()

        elif command.lower() == "create playlist":
            self._library.create_playlist()

        elif command.lower() == "show playlists":
            self._library.show_playlists()

        elif command.lower() == "add to playlist":
            self._library.add_to_playlist(self._account)

        elif command.lower() == "filter playlist":
            self._library.filter_playlist(self._account)

        elif command.lower() == "sort playlist":
            playlist = self._library.select_playlist("sort")
            response = input("Sort tracks by tempo (BPM) in ascending [Y] or descending [N] order? [Y/N]: ")
            if response.lower() == "y":
                ascending_order = True
            elif response.lower() == "n":
                ascending_order = False
            else:
                pass
            playlist.sort_tracks_by_tempo(self._account, ascending_order)

        elif command.lower() == "add to spotify":
            playlist = self._library.select_playlist("add")
            playlist.add_to_spotify(self._account)

        elif command.lower() == "save as csv":
            print("Needs implementation.")

        else:
            print("Please enter a valid command. "
            "Type HELP for a list of available commands.")

    def help(self):
        """Prints all available commands to user"""
        print("""
        Create playlist  --  Create a new playlist.
        Show playlists   --  See all the playlists created during this session.
        Add to playlist  --  Add tracks from your current Spotify playlists to your newly created playlist.
        Filter playlist  --  Filter the tracks in your playlist based on the track tempo or key.
        Sort playlist    --  Sort the tracks in your playlist in ascending or descending order by tempo.
        Add to Spotify   --  Add your newly created playlist to your Spotify library.

        Note: Commands must be entered as they appear, but are not case sensitive.
        """)
