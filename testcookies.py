import yt_dlp

# Define the options
ytdl_opts = {
    'format': 'best',
    'noplaylist': True,
    'cookies' : '/home/ubuntu/omkelthoum/cookies.txt',
    'verbose': True,
}

# Pass the options to YoutubeDL
with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
    # Extract video information
    info = ydl.extract_info("https://www.youtube.com/watch?v=us8gGsb9ZV8", download=False)
    print(info)