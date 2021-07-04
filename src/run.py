"""SpotifyDJ: Command-line interface tools for managing and creating Spotify playlists"""

from .command_parser import CommandParser
from .command_parser import CommandException
from .playlist_library import PlaylistLibrary
from .user_account import UserAccount

if __name__ == "__main__":
    print("""Welcome to SpotifyDJ: A command-line interface for managing and creating Spotify playlists.\nType HELP for list of available commands or EXIT to terminate.\n""")
    playlist_library = PlaylistLibrary()
    user_account = UserAccount()
    user_account.add_user()
    user_account.check_authentication()
    parser = CommandParser(playlist_library, user_account)
    while True:
        command = input("SDJ> ")
        if command.lower() == "exit":
            break
        try:
            parser.execute_command(command) # Might not need to use split but keep for now
        except CommandException as exception:
            print(exception)
    print("SpotifyDJ has terminated.")
