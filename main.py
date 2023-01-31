import time
import base64
import traceback
import spotipy

from spotipy.oauth2 import SpotifyOAuth
from oauth2client.service_account import ServiceAccountCredentials

from config import *
from schedule import *

schedule()
# Returns id of tracks
def get_track_ids(time_frame):
    track_ids = []
    for song in time_frame['items']:
        track_ids.append(song['id'])
    return track_ids


def playlistGen():

    time_ranges = ['short_term', 'medium_term', 'long_term']
    for time_period in time_ranges:

        playlistExists = False

        top_tracks = spot.current_user_top_tracks(
            limit=50, offset=0, time_range=time_period)
        track_ids = get_track_ids(top_tracks)

        period = time_period.replace("_", " ")
    
        playlists = spot.current_user_playlists()
        
        for playlist in playlists['items']:
            if playlist['name'] == f'{period} - Top Tracks': 
                playlist_id = playlist['id']
                # Update songs in existing playlist
                spot.user_playlist_replace_tracks(USERNAME, playlist_id, track_ids)
                spot.user_playlist_change_details(USERNAME, playlist_id, description=f'My Top Played Tracks for {period}. Updated every {time_to_wait} hours.')
                playlistExists = True
                print(f'{period} Top Tracks playlist updated.\n')
                break

        # Create playlist
        if not playlistExists:
            playlist_id = spot.user_playlist_create(USERNAME, f'{period} - Top Tracks', public=True, collaborative=False,
                                                  description=f'My Top Played Tracks for {period}. Updated every {time_to_wait} hours.')['id']
            spot.user_playlist_add_tracks(USERNAME, playlist_id, track_ids)
            with open(f"covers/{time_period}.jpg", 'rb') as image:
                cover_encoded = base64.b64encode(image.read()).decode("utf-8")
            spot.playlist_upload_cover_image(playlist_id, cover_encoded)
            print(f'{period} Top Tracks playlist created.\n')
        print(f'---------------------------------------------------------------------\n')
        

def loop():
    while True:
        try:
            playlistGen()
            print(f'\nNice!!!!\n')
            time.sleep(time_to_wait * 3600)
        except Exception as e:
            print(f'\Exception:\n{e}\n\n{traceback.format_exc()}\n\n')
            time.sleep(600)
            continue

if __name__ == '__main__':
    spot = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT,
        client_secret=SPOTIPY_SECRET_CLIENT,
        redirect_uri=SPOTIPY_REDIRECT,
        scope=SCOPE,
        username=USERNAME,
        open_browser=False))
    loop()