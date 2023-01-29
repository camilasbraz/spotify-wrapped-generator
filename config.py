import os
from dotenv import load_dotenv

#Load dotenv var
load_dotenv()


SPOTIPY_CLIENT = os.environ['CLIENT_ID']
SPOTIPY_SECRET_CLIENT = os.environ['SECRET_CLIENT_ID']
SPOTIPY_REDIRECT = os.environ['REDIRECT_URL']
SCOPE = "user-top-read,playlist-modify-private,playlist-modify-public,user-library-modify,user-library-read,playlist-read-private,ugc-image-upload"
USERNAME = os.environ['USER']
# USERNAME = "camilabraz03"

# How many hours should the program wait until executing again
time_to_wait = 24

