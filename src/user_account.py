"""A user account."""
import os
import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util
from pathlib import Path

class Exception(Exception):
    pass

class UserAccount:
    """A user account class to store credentials and authenticate the account."""
    def __init__(self):

        self._username, self._client_id, self._client_secret, self._redirect_uri = self.get_credentials()
        self._scope = 'playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public'
        self._cache_path = f'{Path(__file__).resolve().parents[1]}/cache/.cache-{self._username}'
        #self._client_id = os.environ.get('SPOTIPY_CLIENT_ID')
        #self._client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
        #self._redirect_uri = 'http://localhost:8080'

    def get_credentials(self):
        """Reads credentials from config.txt"""

        filepath = f'{Path(__file__).resolve().parents[1]}/config.txt'
        with open(filepath) as file:
            lines = file.readlines()
            for line in lines:
                text = line.strip().split(" = ")
                if text[0] == "USERNAME":
                    if text[1] == "your_username":
                        print("Please add your username to SpotifyDJ/config.txt.\n")
                        exit()
                    else:
                        username = text[1]
                elif text[0] == "CLIENT_ID":
                    if text[1] == "your_client_id":
                        print("Please add your Client ID to SpotifyDJ/config.txt.\n")
                        exit()
                    else:
                        client_id = text[1]
                elif text[0] == "CLIENT_SECRET":
                    if text[1] == "your_client_secret":
                        print("Please add your Client Secret to SpotifyDJ/config.txt.\n")
                        exit()
                    else:
                        client_secret = text[1]
                elif text[0] == "REDIRECT_URI":
                    redirect_uri = text[1]

        return(username, client_id, client_secret, redirect_uri)

    def add_user(self):
        """Authenticates user and gets token enabling access to Spotipy library and data"""

        self._token = util.prompt_for_user_token(
            self._username,
            self._scope,
            self._client_id,
            self._client_secret,
            self._redirect_uri,
            cache_path=self._cache_path
            )
        if self._token:
            self._auth_sp = spotipy.Spotify(auth=self._token)
        else:
            print(f"Cannot authenticate account for user {self._username}.\n")

    def check_authentication(self):
        """Checks if authentication was successful"""
        try:
            user_playlist = self._auth_sp.user_playlists(self._username)
        except:
            print("Authentication failed. Please check you entered the correct username.")
            os.remove(f"{self._cache_path}/.cache-{self._username}")
            exit()
