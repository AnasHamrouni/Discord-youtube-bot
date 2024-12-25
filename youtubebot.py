#!/usr/bin/env python3
import re
import discord
from discord.ext import commands
import subprocess
import yt_dlp
import urllib
import asyncio
import threading
import os
import shutil
import sys
import subprocess as sp
from dotenv import load_dotenv
import time
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
PREFIX = os.getenv('BOT_PREFIX', '.')
YTDL_FORMAT = os.getenv('YTDL_FORMAT', 'worstaudio')
PRINT_STACK_TRACE = os.getenv('PRINT_STACK_TRACE', '1').lower() in ('true', 't', '1')
BOT_REPORT_COMMAND_NOT_FOUND = os.getenv('BOT_REPORT_COMMAND_NOT_FOUND', '1').lower() in ('true', 't', '1')
BOT_REPORT_DL_ERROR = os.getenv('BOT_REPORT_DL_ERROR', '0').lower() in ('true', 't', '1')
unix_timestamp = int(time.time())
MAX_SONGS = 10

# Able to reset 7daystodie server
daystodieCommandWhitelist = [322600779078959125,341156433347477504,1138604718365606051,191991730206146562,366585211917697036]
# Oussama troll texts
oussama_troll_texts = [
    "Oussama, did you just discover Twenty One Pilots yesterday?",
    "Oussama, listening to 'Stressed Out' won't finish your homework for you.",
    "Hey Oussama, did you finally learn the lyrics to 'Ride'?",
    "Oussama, are you still trying to figure out what 'Blurryface' means?",
    "Oussama, are you waiting for Twenty One Pilots to write a song about your life?",
    "Oussama, you know 'Heathens' isn't about your social skills, right?",
    "Oussama, did you think 'Car Radio' was a tutorial on how to use one?",
    "Oussama, singing 'Tear In My Heart' won't fix your relationship problems.",
    "Oussama, trying to rap like Tyler Joseph is not a good look for you.",
    "Oussama, stop pretending you're the third member of Twenty One Pilots.",
    "Oussama, did you really just call 'Trench' a trench coat?",
    "Oussama, even 'Blurryface' thinks you should try a new band.",
    "Oussama, no, you can't join Twenty One Pilots by singing in the shower.",
    "Oussama, 'House of Gold' isn't about your Minecraft house.",
    "Oussama, listening to 'Migraine' won't help you understand your headache.",
    "Oussama, did you think 'Hometown' was a shoutout to your city?",
    "Oussama, stop trying to play 'Lane Boy' on repeat, it’s not helping.",
    "Oussama, ‘Goner’ doesn't mean your phone battery is dead.",
    "Oussama, 'Holding on to You' is not about clinging to your phone.",
    "Oussama, did you think 'Polarize' was about your sunglasses?",
]


# Set your Spotify API credentials
client_id  = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Authenticate with Spotify using OAuth
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spoti_api = spotipy.Spotify(client_credentials_manager=client_credentials_manager)




try:
    COLOR = int(os.getenv('BOT_COLOR', 'ff0000'), 16)
except ValueError:
    print('the BOT_COLOR in .env is not a valid hex color')
    print('using default color ff0000')
    COLOR = 0xff0000

bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents(voice_states=True, guilds=True, guild_messages=True, message_content=True))
queues = {} # {server_id: [(vid_file, info), ...]}

def main():
    if TOKEN is None:
        return ("No token provided. Please create a .env file containing the token.\n"
                "For more information view the README.md")

    while True:
        try:
            bot.run(TOKEN)
        except Exception as e:
            print(f"An error occurred: {e}. Restarting bot in 5 seconds...")
            time.sleep(5)  # Wait for 5 seconds before restarting the bot


# @bot.command(name='restartserver', aliases=['rs'])
# async def queue(ctx: commands.Context, *args):

#      if ctx.author.id in daystodieCommandWhitelist:
#           """Kills all running Docker containers and starts the specified Docker container."""
#           try:
#      # Get the list of running Docker container IDs
#                result = sp.run(["sudo", "docker", "ps", "-q"], capture_output=True, text=True, check=True)
#                container_ids = result.stdout.strip()
               
#                # If there are running containers, kill them
#                if container_ids:
#                     container_id_list = container_ids.split()
#                     sp.run(["sudo", "docker", "kill"] + container_id_list, check=True)
#                     await ctx.send("All running Docker containers killed.")
#                command = (
#                     "sudo docker run -d --rm "
#                     "-p 8080:8080/tcp -p 8081:8081/tcp "
#                     "-p 27015:27015/tcp -p 26900:26900/tcp "
#                     "-p 27036:27036/tcp -p 26900:26900/udp "
#                     "-p 26901:26901/udp -p 26902:26902/udp "
#                     "-p 27015:27015/udp -p 27031:27031/udp "
#                     "-p 27032:27032/udp -p 27033:27033/udp "
#                     "-p 27034:27034/udp -p 27035:27035/udp "
#                     "-p 27036:27036/udp "
#                     "-v /home/ubuntu/7daystodie/server:/home/steam/server "
#                     "-v /home/ubuntu/7daystodie/saves:/home/steam/.local/share "
#                     "7days"
#                )

#                # Start the specified Docker container
#                sp.run(command, check=True, shell=True)
#                await ctx.send("Docker container started successfully.")
#           except sp.CalledProcessError as e:
#                await ctx.send(f"Error: {e}")
#      else:
#           await ctx.send("NICE TRY")

@bot.command(name='queue', aliases=['q'])
async def queue(ctx: commands.Context, *args):
     try:
          queue = queues[ctx.guild.id]
     except KeyError:
          queue = None

     if not queue:
          await ctx.send("The bot isn't playing anything.")
          return

     title_str = lambda val: '‣ %s\n\n' % val[1] if val[0] == 0 else '**%2d:** %s\n' % val
     queue_str = ''.join(map(title_str, enumerate([i[1]["title"] for i in queue])))

     if len(queue_str) > 800:  # Truncate if longer than 1020 characters
          queue_str = queue_str[:800] + "... (more items in queue)"

     embedVar = discord.Embed(color=COLOR)
     embedVar.add_field(name='Now playing:', value=queue_str, inline=False)
     await ctx.send(embed=embedVar)

     if not await sense_checks(ctx):
          return



@bot.command(name='pop', aliases=['pp'])
async def pop(ctx, *args):
    queue = queues.get(ctx.guild.id)
    if not queue:
        await ctx.send("The bot isn't playing anything.")
        return
    if not args:
        await ctx.send("Please specify the song number to remove. Example: .pop 5")
        return
    try:
        songNumber = int(args[0])
        if 0 <= songNumber < len(queue):
            removed_song = queue.pop(songNumber)
            await ctx.send(f"Removed song number {songNumber} from the queue.")
        else:
            await ctx.send(f"Song number {songNumber} doesn't exist in the queue.")
    except ValueError:
        await ctx.send("Please provide a valid song number. Example: .pop 5")


@bot.command(name='shuffle', aliases=['sh'])
async def shuffle(ctx):
    # Retrieve the queue for the current guild
    queue = queues.get(ctx.guild.id)

    # Check if the queue exists and has more than two songs (to leave the first in place and shuffle the rest)
    if queue and len(queue) > 2:
        first_song = queue.pop(0)  # Remove the first song and keep it aside
        random.shuffle(queue)  # Shuffle the remaining songs in the queue
        queue.insert(0, first_song)  # Reinsert the first song at the beginning
        await ctx.send("The queue has been shuffled.")
    elif queue and len(queue) <= 2:
        await ctx.send("Not enough songs in the queue to shuffle.")
    else:
        await ctx.send("There's nothing in the queue to shuffle.")
@bot.command(name='pause', aliases=['pa'])
async def pause(ctx):
    voice_client = ctx.guild.voice_client

    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Music has been paused.")
    else:
        await ctx.send("There is no music currently playing.")

@bot.command(name='resume', aliases=['r'])
async def resume(ctx):
    voice_client = ctx.guild.voice_client

    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await ctx.send("Music has been resumed.")
    else:
        await ctx.send("Music is not paused or there is no active music.")

@bot.command(name='skip', aliases=['s'])
async def skip(ctx: commands.Context, *args):
     try: queue_length = len(queues[ctx.guild.id])
     except KeyError: queue_length = 0
     if queue_length <= 0:
          await ctx.send('the bot isn\'t playing anything')
          return
     if not await sense_checks(ctx):
          return

     try: n_skips = int(args[0])
     except IndexError:
          n_skips = 1
     except ValueError:
          if args[0] == 'all': n_skips = queue_length
          else: n_skips = 1
     if n_skips == 1:
          message = 'skipping track'
     elif n_skips < queue_length:
          message = f'skipping `{n_skips}` of `{queue_length}` tracks'
     else:
          message = 'skipping all tracks'
          n_skips = queue_length
     await ctx.send(message)

     voice_client = get_voice_client_from_channel_id(ctx.author.voice.channel.id)
     for _ in range(n_skips - 1):
          queues[ctx.guild.id].pop(0)
     voice_client.stop()

@bot.command(name='play', aliases=['p'])
async def play(ctx: commands.Context, *args):

     if ctx.author.id == 315985768957083648:
          if random.randint(0, 1) == 1:
               random_joke_number = random.randint(0, 19)
               await ctx.send(oussama_troll_texts[random_joke_number])

     # This is used to be used for LEAGUE of legends bot so the bot joins my channel. can be removed just keep the else as the main action
     if ctx.author.id == 1197649089735688293:
          member = ctx.guild.get_member(341156433347477504)
          voice_state = member.voice
     else:
          voice_state = ctx.author.voice

     if not await sense_checks(ctx, voice_state=voice_state):
          return
     query = ' '.join(args)
     if query == "":
          if ctx.author.id == 274977675884363798:
               await ctx.send('YA KROKO YA 5RA. MUTED AND REPORTED.')
               return
          else:
               await ctx.send('Invalid song name')
               return
     # this is how it's determined if the url is valid (i.e. whether to search or not) under the hood of yt-dlp
     will_need_search = not urllib.parse.urlparse(query).scheme

     server_id = ctx.guild.id

     ytdl_format_options = {'format': YTDL_FORMAT,
                         'source_address': '0.0.0.0',
                         'quiet': True,
                         'default_search': 'ytsearch',
                         'outtmpl': '%(id)s.%(ext)s',
                         'noplaylist': False,
                         'playlistend': MAX_SONGS,
                         'cookiefile' : './cookies.txt',
                         'verbose': True,
                         
                         # 'progress_hooks': [lambda info, ctx=ctx: video_progress_hook(ctx, info)],
                         # 'match_filter': lambda info, incomplete, will_need_search=will_need_search, ctx=ctx: start_hook(ctx, info, incomplete, will_need_search),
                         'paths': {'home': f'./dl/{server_id}'}}

     with yt_dlp.YoutubeDL(ytdl_format_options) as ydl:
          # source address as 0.0.0.0 to force ipv4 because ipv6 breaks it for some reason
          # this is equivalent to --force-ipv4 (line 312 of https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/options.py)
          #await ctx.send(f'looking for `{query}`...')
          if "spotify" in query:
               if "track" in query:
                    # Extract the track ID from the URL
                    track_id = query.split("/")[-1].split("?")[0]
                    # Fetch the track's details
                    track = spoti_api.track(track_id)
                    # Print the track's name
                    artists = [artist['name'] for artist in track['artists']]
                    song_search_query = ', '.join(artists) +" "+ track['name']
                    await play(ctx, song_search_query)
                    return
               else:
                    playlist_id = query.split("/")[-1].split("?")[0]
                    # Fetch the playlist's details
                    playlist = spoti_api.playlist_tracks(playlist_id)

                    # Iterate through the tracks in the playlist
                    for item in playlist['items'][:MAX_SONGS]:
                         track = item['track']
                         artists = [artist['name'] for artist in track['artists']]
                         song_search_query = ', '.join(artists) + " " + track['name']

                         # Enqueue or play each track
                         # Note: Depending on your bot's design, you might need to enqueue these tracks
                         # or play them directly. The following line is a placeholder to indicate where
                         # you would handle each track.
                         await play(ctx, song_search_query)
                    return

          else:
               if "list" in query:
                    try:
                         info = ydl.extract_info(query, download=False)
                    except yt_dlp.utils.DownloadError as err:
                         await notify_about_failure(ctx, err)
                         return
                    if 'entries' in info:
                    # Limit the number of entries to MAX_SONGS to handle playlists larger than MAX_SONGS
                         for i in range(MAX_SONGS):
                              entry = info['entries'][i]
                              # send link if it was a search, otherwise send title as sending link again would clutter chat with previews
                              # await ctx.send('downloading ' + (f'https://youtu.be/{entry["id"]}' if will_need_search else f'`{entry["title"]}`'))
                              # download the query as a list of songs (checks if the song has been already downloaded)
                              # TODO fix downloading multiple times
                              await play(ctx, f"https://youtu.be/{entry['id']}")
               else:
                    try:
                         await ctx.send('strating data collector')
                         info = ydl.extract_info(query, download=False)
                         await ctx.send('Got data')
                    except yt_dlp.utils.DownloadError as err:
                         await notify_about_failure(ctx, err)
                         return

                    if 'entries' in info:
                         info = info['entries'][0]
                    # send link if it was a search, otherwise send title as sending link again would clutter chat with previews
                    await ctx.send('adding ' + f'`{info["title"]}` to the queue')
                    try: 
                         ydl.download([query])
                    except yt_dlp.utils.DownloadError as err:
                         await notify_about_failure(ctx, err)
                         return

                    path = f'./dl/{server_id}/{info["id"]}.{info["ext"]}'
                    try: queues[server_id].append((path, info))
                    except KeyError: # first in queue
                         queues[server_id] = [(path, info)]
                         try: connection = await voice_state.channel.connect()
                         except discord.ClientException: connection = get_voice_client_from_channel_id(voice_state.channel.id)
                         connection.play(discord.FFmpegOpusAudio(path), after=lambda error=None, connection=connection, server_id=server_id:
                                                                           after_track(error, connection, server_id))
     




def get_voice_client_from_channel_id(channel_id: int):
     for voice_client in bot.voice_clients:
          if voice_client.channel.id == channel_id:
               return voice_client

def after_track(error, connection, server_id):
     if error is not None:
          print(error)
     try: path = queues[server_id].pop(0)[0]
     except KeyError: return # probably got disconnected
     if path not in [i[0] for i in queues[server_id]]: # check that the same video isn't queued multiple times
          try: os.remove(path)
          except FileNotFoundError: pass
     try:
          connection.play(discord.FFmpegOpusAudio(queues[server_id][0][0]), after=lambda error=None, connection=connection, server_id=server_id:
                                                                           after_track(error, connection, server_id))

     except IndexError: # that was the last item in queue
          unix_timestamp = int(time.time())
          queues.pop(server_id) # directory will be deleted on disconnect
          asyncio.run_coroutine_threadsafe(safe_disconnect(connection), bot.loop).result()

async def safe_disconnect(connection):
     await asyncio.sleep(910)
     if not connection.is_playing() and (int(time.time()) - unix_timestamp) > 900:
          await connection.disconnect()

async def sense_checks(ctx: commands.Context, voice_state=None) -> bool:
     if voice_state is None: voice_state = ctx.author.voice
     if voice_state is None:
          await ctx.send('you have to be in a voice channel to use this command')
          return False

     if bot.user.id not in [member.id for member in voice_state.channel.members] and ctx.guild.id in queues.keys():
          await ctx.send('you have to be in the same voice channel as the bot to use this command')
          return False
     return True

@bot.event
async def on_voice_state_update(member: discord.User, before: discord.VoiceState, after: discord.VoiceState):
     if member != bot.user:
          return
     if before.channel is None and after.channel is not None: # joined vc
          return
     if before.channel is not None and after.channel is None: # disconnected from vc
          # clean up
          server_id = before.channel.guild.id
          try: queues.pop(server_id)
          except KeyError: pass
          try: shutil.rmtree(f'./dl/{server_id}/')
          except FileNotFoundError: pass
     # Moved to a different voice channel within the same server
     if before.channel != after.channel and before.channel is not None and after.channel is not None:
          voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
          if voice_client and voice_client.is_playing():
               await voice_client.move_to(after.channel)
               # Stop the current playback
               voice_client.pause()
               await asyncio.sleep(1)
               voice_client.resume()


@bot.event
async def on_command_error(ctx: discord.ext.commands.Context, err: discord.ext.commands.CommandError):
     # now we can handle command errors
     if isinstance(err, discord.ext.commands.errors.CommandNotFound):
          if BOT_REPORT_COMMAND_NOT_FOUND:
               await ctx.send("command not recognized. To see available commands type {}help".format(PREFIX))
          return

     # we ran out of handlable exceptions, re-start. type_ and value are None for these
     sys.stderr.write(f'unhandled command error raised, {err=}')
     sys.stderr.flush()
     sp.run(['./restart'])

@bot.event
async def on_ready():
     print(f'logged in successfully as {bot.user.name}')
async def notify_about_failure(ctx: commands.Context, err: yt_dlp.utils.DownloadError):
     if BOT_REPORT_DL_ERROR:
          # remove shell colors for discord message
          sanitized = re.compile(r'\x1b[^m]*m').sub('', err.msg).strip()
          if sanitized[0:5].lower() == "error":
               # if message starts with error, strip it to avoid being redundant
               sanitized = sanitized[5:].strip(" :")
          await ctx.send('failed to download due to error: {}'.format(sanitized))
     else:
          await ctx.send('sorry, failed to download this video')
     return

@bot.event
async def on_message(message):
     # Define the channel ID where commands should be listened to
     allowed_channels_id = [538987905947926559,1121048498578665563,1212885887948431380,1033076184931639409]  # Replace with your desired channel ID

     # Check if the message is in the allowed channel
     if message.channel.id not in allowed_channels_id:
          return
     if message.author.bot and message.author.id != 1197649089735688293:
          return
     '''
     if message.author.id == 1197649089735688293:
          ctx = await bot.get_context(message)
          if ctx.valid:
               # Extract the command and arguments from the message
               command = message.content[len(PREFIX):].split(' ')[0]
               args = message.content.split(' ')[1:]

               # Manually invoke the corresponding command function
               if command == 'play':
                    await play(ctx, *args)
                    return
               elif command == 'skip':
                    await skip(ctx, *args)
                    return
               elif command == 'queue':
                    await queue(ctx, *args)
     '''
     await bot.process_commands(message)




if __name__ == '__main__':
     try:
          sys.exit(main())
     except SystemError as error:
          if PRINT_STACK_TRACE:
               raise
          else:
               print(error)
