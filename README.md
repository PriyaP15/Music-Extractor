# Music Extractor

Music Extractor is a project that demonstrates how to fetch Spotify playlists and download the songs for offline listening without requiring Spotify Premium. Using this project, users can export all their playlists into CSV files and then download the corresponding tracks from YouTube as high-quality MP3 files.

The project consists of two main Python scripts:

1. **get_my_spotify_songs.py** – Connects to a Spotify account, retrieves all playlists, and saves each playlist’s songs (name, artist, album, and Spotify URL) into CSV files.

2. **download_from_csv.py** – Reads the CSV files, searches YouTube for each track, and downloads the audio as MP3 files. Downloads are automatically organized into folders corresponding to each playlist, preserving the original structure.

Through this project, users can experience their Spotify playlists offline, maintain the organization of their music collection, and explore how Spotify and YouTube data can be combined programmatically. It also handles issues like invalid filenames, network timeouts, and ensures smooth offline access to music.

Music Extractor serves as an educational project that demonstrates automation, API usage, and media handling while providing practical offline music access.

---

## Project Structure

```
Music-Extractor/
│── get_my_spotify_songs.py
│── .gitignore
│── .env.example
│── download_from_csv.py
│── requirements.txt
│── README.md
│── .env
│── Playlists/
│── Downloads/
```

* **Playlists/** contains exported playlist CSVs
* **Downloads/** contains MP3 files organized by playlist
* `.env` contains your Spotify API keys

---

## Installation

### 1. Install Python dependencies

```
pip install -r requirements.txt
```

### 2. Install FFmpeg (Required)

Download FFmpeg for Windows (Essentials build):
[https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)

Extract it anywhere, then update the path inside `download_from_csv.py`:

```python
ffmpeg_location = r"C:\Path\To\ffmpeg\bin"
```

Ensure the `bin` folder contains:

* ffmpeg.exe
* ffprobe.exe

---

## Spotify API Setup

1. Go to: [https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Create a new App.
3. Add this Redirect URI:

```
http://127.0.0.1:8080
```

4. Create a `.env` file in your project folder:

```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
REDIRECT_URI=http://127.0.0.1:8080
```

---

## Usage

### Step 1 — Export Spotify Playlists to CSV

Run:

```
python get_my_spotify_songs.py
```

This creates CSV files in:

```
Playlists/
   ├── My Playlist.csv
   ├── Chill Mix.csv
   └── ...
```

### Step 2 — Download MP3s From CSV

Run:

```
python download_from_csv.py
```

This generates MP3 files in:

```
Downloads/
   ├── My Playlist/
   │     ├── song1.mp3
   │     ├── song2.mp3
   ├── Chill Mix/
   │     ├── track1.mp3
```

---

## FFmpeg Troubleshooting

**Error: “ffmpeg not found”**

* Ensure the path in `download_from_csv.py` is correct:

```python
ffmpeg_location = r"C:\yourpath\ffmpeg\bin"
```

* Make sure `ffmpeg.exe` and `ffprobe.exe` exist in that folder.

**Error: “Permission denied”**

Run PowerShell or CMD as Administrator.

---

## Spotify Troubleshooting

**Spotify login keeps failing**

Delete cached tokens:

```
rm .cache*
```

(Windows: search for `.cache` in your project folder and delete it.)

**Spotify API timeout or 429**

* The script automatically retries.
* Avoid running too many requests too quickly.

---

## Tips

* Spotify Premium is not required.
* YouTube API keys are not required — the project uses direct search via yt-dlp.
* The script automatically sanitizes illegal Windows filename characters.

---

## Requirements

See `requirements.txt`:

```
spotipy
python-dotenv
yt-dlp
requests
urllib3
```

---

## License

This project is free to use, modify, and distribute.
