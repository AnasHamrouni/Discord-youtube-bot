#!/usr/bin/env python3
import yt_dlp
import urllib
import os

YTDL_FORMAT = os.getenv('YTDL_FORMAT', 'worstaudio')
server_id = "123123"
queues = {}  # {server_id: [(vid_file, info), ...]}
MAX_SONGS = 4  # Limit the number of songs from the playlist

def main():
    test = "https://www.youtube.com/watch?v=4JPyS_nGVT8"
    query = "https://www.youtube.com/watch?v=4JPyS_nGVT8"
    # Determine if the URL is valid
    will_need_search = not urllib.parse.urlparse(query).scheme

    with yt_dlp.YoutubeDL({'format': YTDL_FORMAT,
                           'source_address': '0.0.0.0',  # Force IPv4
                           'default_search': 'ytsearch',
                           'outtmpl': '%(id)s.%(ext)s',
                           'noplaylist': False,  # Changed to False to allow playlist download
                           'playlistend': MAX_SONGS,  # Limit the number of videos downloaded from the playlist
                           'paths': {'home': f'./dl/{server_id}'}}) as ydl:
        try:
            # Extract information without downloading
            info = ydl.extract_info(query, download=False)
        except yt_dlp.utils.DownloadError as err:
            print("Download error")
            return

        # If it's a playlist, info will contain 'entries'
        if 'entries' in info:
            # Limit the number of entries to MAX_SONGS to handle playlists larger than MAX_SONGS
            entries = info['entries'][:MAX_SONGS]
            for entry in entries:
                print("LIST OF SONGS")
                print('Downloading ' +  f'`{entry["title"]}`')
                print(f'https://youtu.be/{entry["id"]}')

if __name__ == "__main__":
    main()
