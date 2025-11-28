import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv
import os
import re
from dotenv import load_dotenv
import sys

sys.stdout.reconfigure(line_buffering=True)

# Load credentials from .env
load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = "user-library-read playlist-read-private playlist-read-collaborative"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    open_browser=True
))

def sanitize_filename(name):
    """Replace invalid Windows filename characters"""
    return re.sub(r'[<>:"/\\|?*]', '-', name)

def fetch_liked_songs():
    print("Fetching liked songs...")
    songs = []
    results = sp.current_user_saved_tracks(limit=50)
    while results:
        for item in results['items']:
            track = item['track']
            if track and "spotify" in track.get("external_urls", {}):
                songs.append(track)
        if results["next"]:
            results = sp.next(results)
        else:
            break
    return songs

def fetch_playlist_songs():
    print("Fetching playlists...")
    playlists = sp.current_user_playlists(limit=50)
    playlist_tracks = {}

    while playlists:
        for pl in playlists['items']:
            pl_name = sanitize_filename(pl['name'])
            print(f"Fetching playlist: {pl_name}")
            tracks = []
            results = sp.playlist_items(pl['id'], limit=100)
            while results:
                for item in results['items']:
                    track = item['track']
                    if track and "spotify" in track.get("external_urls", {}):
                        tracks.append(track)
                if results["next"]:
                    results = sp.next(results)
                else:
                    break
            playlist_tracks[pl_name] = tracks
        if playlists["next"]:
            playlists = sp.next(playlists)
        else:
            break

    return playlist_tracks

def save_songs_by_playlist(playlist_tracks):
    print("Saving CSVs for each playlist...")
    os.makedirs("Playlists", exist_ok=True)

    for playlist_name, tracks in playlist_tracks.items():
        filename = os.path.join("Playlists", f"{playlist_name}.csv")
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "artists", "album", "url"])
            for t in tracks:
                artists = ", ".join(a["name"] for a in t["artists"])
                writer.writerow([t["name"], artists, t["album"]["name"], t["external_urls"]["spotify"]])
        print(f"Saved: {filename}")

if __name__ == "__main__":
    # Include liked songs as a special playlist
    liked_songs = fetch_liked_songs()
    playlist_tracks = {"Liked Songs": liked_songs}

    # Add all playlists
    playlist_tracks.update(fetch_playlist_songs())

    save_songs_by_playlist(playlist_tracks)
