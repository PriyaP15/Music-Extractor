import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv
import os
import re
import time
from dotenv import load_dotenv
import sys

sys.stdout.reconfigure(line_buffering=True)

# Load credentials
load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

SCOPE = "user-library-read playlist-read-private playlist-read-collaborative"

# ----------------------------------------------------
# SAFE SPOTIFY CLIENT WITH LONG TIMEOUT + RETRIES
# ----------------------------------------------------

def create_sp_client():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            open_browser=True
        ),
        requests_timeout=30     # <-- IMPORTANT : avoids timeouts
    )

sp = create_sp_client()


# ----------------------------------------------------
# Retry wrapper for any Spotify API call
# ----------------------------------------------------
def safe_call(func, *args, retries=5, **kwargs):
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)

        except Exception as e:
            print(f"⚠ Spotify timeout/error — retrying ({attempt+1}/{retries})...")
            print("   Error:", e)
            time.sleep(3)

    print("❌ Failed after multiple retries — network too unstable.")
    return None


# ----------------------------------------------------
# Clean filenames for Windows
# ----------------------------------------------------
def sanitize_filename(name):
    if not name or name.strip() == "":
        return "Unknown_Playlist"
    name = re.sub(r'[<>:"/\\|?*]', '-', name)
    return name.strip()


# ----------------------------------------------------
# Fetch playlist songs with retry
# ----------------------------------------------------
def fetch_playlist_songs():
    print("Fetching playlists...")

    playlists = safe_call(sp.current_user_playlists, limit=50)
    if playlists is None:
        return {}

    playlist_tracks = {}

    while playlists:
        for pl in playlists["items"]:

            pl_name = sanitize_filename(pl.get("name", "Unknown"))
            print(f"📁 Playlist: {pl_name}")

            tracks = []

            results = safe_call(sp.playlist_items, pl["id"], limit=100)
            if results is None:
                continue

            while results:
                for item in results.get("items", []):
                    track = item.get("track")
                    if track and "spotify" in track.get("external_urls", {}):
                        tracks.append(track)

                if results.get("next"):
                    results = safe_call(sp.next, results)
                else:
                    break

            playlist_tracks[pl_name] = tracks

        if playlists.get("next"):
            playlists = safe_call(sp.next, playlists)
        else:
            break

    return playlist_tracks


# ----------------------------------------------------
# Save CSVs for each playlist
# ----------------------------------------------------
def save_songs_by_playlist(playlist_tracks):
    print("Saving CSVs for each playlist...")
    os.makedirs("Playlists", exist_ok=True)

    for playlist_name, tracks in playlist_tracks.items():

        filename = os.path.join("Playlists", f"{playlist_name}.csv")

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "artists", "album", "url"])

            for t in tracks:
                name = t.get("name", "")
                artists = ", ".join(a["name"] for a in t.get("artists", []))
                album = t.get("album", {}).get("name", "")
                url = t.get("external_urls", {}).get("spotify", "")

                writer.writerow([name, artists, album, url])

        print(f"✔ Saved: {filename}")


# ----------------------------------------------------
# MAIN
# ----------------------------------------------------
if __name__ == "__main__":
    playlist_tracks = fetch_playlist_songs()
    save_songs_by_playlist(playlist_tracks)
    print("\n🎉 Done! CSVs saved inside the 'Playlists' folder.\n")
