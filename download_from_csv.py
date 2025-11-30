import os
import csv
from yt_dlp import YoutubeDL

PLAYLISTS_FOLDER = "Playlists"

# --- yt-dlp options ---
YDL_OPTS = {
    "format": "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
    "ffmpeg_location": r"C:\Users\priya\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin",
    "quiet": False,
}


def download_track(query, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    opts = YDL_OPTS.copy()
    opts["outtmpl"] = f"{output_folder}/%(title)s.%(ext)s"

    with YoutubeDL(opts) as ydl:
        print(f"🔎 Searching: {query}")
        ydl.download([f"ytsearch:{query}"])


def process_csv(csv_path):
    playlist_name = os.path.splitext(os.path.basename(csv_path))[0]
    output_folder = os.path.join("Downloads", playlist_name)

    print(f"\n📁 Processing playlist: {playlist_name}")

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            track = row.get("name", "").strip()
            artists = row.get("artists", "").strip()

            if not track:
                print("Skipping empty track...")
                continue

            query = f"{track} {artists} audio"
            download_track(query, output_folder)


def main():
    for file in os.listdir(PLAYLISTS_FOLDER):
        if file.lower().endswith(".csv"):
            csv_path = os.path.join(PLAYLISTS_FOLDER, file)
            process_csv(csv_path)


if __name__ == "__main__":
    main()
