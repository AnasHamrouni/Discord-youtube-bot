from yt_dlp import YoutubeDL

# Define options, including the path to your cookies file
ytdl_opts = {
    'format': 'best',
    'verbose': True,  # To enable detailed logs (equivalent to `-vU`)
    'cookies': './cookies.txt',  # Ensure the path matches your command line
}

# Use the options with YoutubeDL
with YoutubeDL(ytdl_opts) as ydl:
    # Extract video information without downloading
    info = ydl.extract_info("https://www.youtube.com/watch?v=4w9iDLuvSOQ", download=False)

    # Print the extracted info (for testing)
    print(info)