# Imports
# -*- coding: utf-8 -*-
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import sys
import os
from datetime import datetime
import csv

def authenticateUser(username):

    #sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    id = os.environ.get('SPOTIPY_CLIENT_ID') # Use if you've set these environment variable in your .bash_rc, otherwise hardcode it here
    secret = os.environ.get('SPOTIPY_CLIENT_SECRET') # Use if you've set these environment variable in your .bash_rc, otherwise hardcode it here
    uri = 'http://localhost:8080'
    scope = 'playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public'
    token = util.prompt_for_user_token(username, scope, id, secret, uri)
    if token:
        sp = spotipy.Spotify(auth=token)
        return(sp)
    else:
        print("Cannot get token for ", username)


def getUserPlaylist(playlistName): # Given playlist name, returns playlist ID

    allPlaylists = sp.user_playlists(username)
    for i, item in enumerate(allPlaylists['items']):
        name = item['name']
        if name == playlistName:
            playlistID = item['id']
            return(playlistID)

    return("Cannot find playlist ", playlistName)


def getTrackData(playlistID): # Given playlist ID, returns a list of dictionary items. Need to add trackID.

    trackData = []
    startIndex = 0
    endIndex = 99

    while endIndex == 99:

        allTracks = sp.playlist_tracks(playlistID,offset=startIndex,limit=100)

        for i, item in enumerate(allTracks['items']):

            trackDict = {'Album':[],'Artist':[],'Released':[],'Genre':[],'Title':[],'Duration':[],'BPM':[],'Key':[]}
            track = item['track']
            trackDict['Title'] = track['name']
            trackDict['Artist'] = track['artists'][0]['name']
            trackDict['Album'] = track['album']['name']
            artistID = sp.artist(track['artists'][0]['external_urls']['spotify'])
            trackGenres = " / ".join(artistID['genres'])
            trackDict['Genre'] = trackGenres.title()
            trackDict['Released'] = track['album']['release_date']
            trackDict['Duration'] = datetime.fromtimestamp(track['duration_ms']/1000).strftime("%M:%S")
            trackDict['BPM'] = sp.audio_features([track['id']])[0]['tempo']
            trackDict['Key'] = sp.audio_features([track['id']])[0]['key'],sp.audio_features([track['id']])[0]['mode']

            trackData.append(trackDict)

        endIndex = i
        startIndex=startIndex+100

    trackData = convertKeys(trackData)
    return(trackData)


def getTrackIDs(playlistID,sp):

    trackIDs = []
    startIndex = 0
    endIndex = 99
    while endIndex == 99:
        allTracks = sp.playlist_tracks(playlistID,offset=startIndex,limit=100)
        for i, item in enumerate(allTracks['items']):
            trackIDs.append(item['track']['id'])
        endIndex = i
        startIndex=startIndex+100

    return(trackIDs)


def convertKeys(trackData): # Convert spotify key to tonal and camelot

    camelotDict = {'0,1':'8B','1,1':'3B','2,1':'10B','3,1':'5B','4,1':'12B','5,1':'7B','6,1':'2B','7,1':'9B','8,1':'4B','9,1':'11B','10,1':'6B','11,1':'1B',
        '0,0':'5A','1,0':'12A','2,0':'7A','3,0':'2A','4,0':'9A','5,0':'4A','6,0':'11A','7,0':'6A','8,0':'1A','9,0':'8A','10,0':'3A','11,0':'10A'}

    tonalDict = {'8B':'C, B♯','3B':'C♯, D♭','10B':'D','5B':'D♯, E♭','12B':'E','7B':'F','2B':'F♯, G♭','9B':'G','4B':'G♯, A♭','11B':'A','6B':'A♯, B♭','1B':'B','5A':'Cm','12A':'D♭m','7A':'Dm','2A':'E♭m','9A':'Em','4A':'Fm','11A':'G♭m','6A':'Gm','1A':'A♭m','8A':'Am','3':'B♭m','10A':'Bm'}

    for i in range(len(trackData)):
        spotifyKey = ','.join(map(str,trackData[i]['Key']))
        camelotKey = camelotDict.get(spotifyKey)
        tonalKey = tonalDict.get(camelotKey)
        trackData[i]['Camelot Key'] = camelotKey
        trackData[i]['Tonal Key'] = tonalKey
        del trackData[i]['Key']

    return(trackData)

camelotDict = {'0,1':'8B','1,1':'3B','2,1':'10B','3,1':'5B','4,1':'12B','5,1':'7B','6,1':'2B','7,1':'9B','8,1':'4B','9,1':'11B','10,1':'6B','11,1':'1B',
    '0,0':'5A','1,0':'12A','2,0':'7A','3,0':'2A','4,0':'9A','5,0':'4A','6,0':'11A','7,0':'6A','8,0':'1A','9,0':'8A','10,0':'3A','11,0':'10A'}

tonalDict = {'8B':'C, B♯','3B':'C♯, D♭','10B':'D','5B':'D♯, E♭','12B':'E','7B':'F','2B':'F♯, G♭','9B':'G','4B':'G♯, A♭','11B':'A','6B':'A♯, B♭','1B':'B','5A':'Cm','12A':'D♭m','7A':'Dm','2A':'E♭m','9A':'Em','4A':'Fm','11A':'G♭m','6A':'Gm','1A':'A♭m','8A':'Am','3':'B♭m','10A':'Bm'}

def camelotToSp(camelotDict,values):
    output = list()
    itemsList = camelotDict.items()
    for item  in itemsList:
        if item[1] in values:
            output.append(item[0])
    return  output

def saveTrackData(trackData,outPath,playlistName):

    csvFile = "{}/{}TrackData.csv".format(outPath,playlistName)
    csvColumns = list(trackData[0].keys())

    with open(csvFile, "w") as file:
        writer = csv.DictWriter(file, fieldnames=csvColumns)
        writer.writeheader()
        for row in trackData:
            writer.writerow(row)


def filterPlaylists(username,sp):

    userPlaylists = sp.user_playlists(username)
    playlistID = []
    allTracks = []

    for i, item in enumerate(userPlaylists['items']):
        print("{0:4d}  {1}".format(i,item['name']))
        playlistID.append(item['id'])

    playlistSelection = formatSelection(playlistID,tonalDict,input("\nSelect playlist by number [e.g. 2,3,4], range [e.g. 2:4] or type ALL: "),type="playlist")

    bpmSelection = formatSelection(playlistID,tonalDict,input("Enter BPM range [e.g. 100:120] or type ALL: "),type="bpm")

    for i, k in enumerate(tonalDict):
        print("{0:4d}  {1}".format(i,tonalDict[k]))
    keySelection = formatSelection(playlistID,tonalDict,input("\nSelect key(s) by number [e.g. 5,6], range [e.g. 5:6] or type ALL: "),type="key")
    #exportData = input("Export track data to .csv? [Y/N]: ")

    saveName = input("Name for your playlist: ")
    #print("Grab a cuppa; this could take a while...") # Maybe only if number playlists > 3 and exportData is selected

    for i, item in enumerate(playlistSelection):
        allTracks.append(getTrackIDs(item,sp))
        #print("Playlist {}/{} processed".format(i+1,len(playlistSelection)))

    allTracks = [item for sublist in allTracks for item in sublist]
    filtTracks = filterTracks(allTracks,bpmSelection,keySelection,sp)
    createPlaylist(username,filtTracks,saveName,bpmSelection,keySelection,sp)
    # if exportData in ["Y","y","yes"]:
    #     saveTrackData(filtTracks,outPath,saveName)


def createPlaylist(username,tracks,playlistName,bpm,key,sp):

    sp.user_playlist_create(username,playlistName,public=False,collaborative=False,description='A selection of tracks between {} and {} BPM in {} key. Made using Spotipy.'.format(bpm[0],bpm[1],", ".join(key)))
    playlistID = getUserPlaylist(playlistName)
    sp.playlist_add_items(playlistID,tracks,position=None)


def filterTracks(tracks,bpmRange,keys,sp): # Given list of track IDs {tracks}, return a list of track IDs with BPM within {bpmRange} and key one of {keys}

    filteredTracks = []
    bpmMin, bpmMax = bpmRange[0], bpmRange[1]
    for track in tracks:
        bpm = sp.audio_features([track])[0]['tempo']
        key = sp.audio_features([track])[0]['key']
        mode = sp.audio_features([track])[0]['mode']
        spKey="{},{}".format(key,mode)
        userKeys=camelotToSp(camelotDict,keys)
        if bpm >= bpmMin and bpm < bpmMax and spKey in userKeys:
            filteredTracks.append(track)

    if len(filteredTracks) > 0:
        return(filteredTracks)
    else:
        print("No tracks from the selected playlists matched your criteria. Select different playlists or change BPM and/or key selections.")
        exit()


def formatSelection(playlistID,keys,userInput,type): # TO DO. Must output list containing indices or values

    if ':' in userInput:
        intRange = [*map(int,userInput.split(":"))]
        indexList = list(range(intRange[0],intRange[1]+1))
        if type == 'playlist':
            formattedSelection = [playlistID[i] for i in indexList]
        elif type == 'key':
            formattedSelection = [list(tonalDict.keys())[i] for i in indexList]
        else:
            formattedSelection = [*map(float,intRange)]
        return(formattedSelection)

    elif ',' in userInput:
        indexList = [*map(int,userInput.split(","))]
        if type == 'playlist':
            formattedSelection = [playlistID[i] for i in indexList]
        elif type == 'key':
            formattedSelection = [list(tonalDict.keys())[i] for i in indexList]
        else:
            formattedSelection = [*map(float,indexList)]
        return(formattedSelection)

    elif userInput in ["ALL","All","all"]:
        if type == 'playlist':
            formattedSelection = playlistID[:]
        elif type == 'key':
            formattedSelection = list(tonalDict.keys())
        else:
            formattedSelection = [0.0,1000.0]
        return(formattedSelection)

    else:
        if type == 'playlist':
            formattedSelection = [playlistID[int(userInput)]]
        elif type == 'key':
            formattedSelection = [list(tonalDict.keys())[int(userInput)]]
        else:
            formattedSelection = [float(userInput)]
        return(formattedSelection)

