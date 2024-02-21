### BASED ON https://github.com/maxcutlyp/YoutubeBot, MANY THANKS <3

### Introduction
Welcome to the MusicBot repository! This Discord bot is designed to enrich your server by offering the capability to play music from both YouTube and Spotify directly in your voice channels. It's an ideal tool for creating shared music experiences, whether you're looking to enjoy background music during gaming sessions, host a virtual listening party, or simply share your favorite tunes with friends. This guide will walk you through setting up this versatile music bot for your community.

## Features
- **Play Command**: Use `.play {url or search term}` to play music from YouTube or Spotify. You can input a direct video/link or search for music by name. The bot will join a voice channel (VC) if it's not already in one.
  - Alternate command: `.p`
- **Pause Command**: Use `.pause` to temporarily stop the currently playing track. You can resume playback with the resume command.
  - Alternate command: `.pa`
- **Resume Command**: Use `.resume` to continue playing the paused track from where it left off.
  - Alternate command: `.r`
- **Skip Command**: Use `.skip {n}` to advance through the queue by a specified number of tracks. If no number is provided, it skips the current track. Use `.skip all` to clear the queue and leave the VC.
  - Alternate command: `.s`
- **Queue Command**: Use `.queue` to view the upcoming tracks queued for playback.
  - Alternate command: `.q`
- **Shuffle Command**: Use `.shuffle` to mix up the order of the queued tracks, adding an element of unpredictability to your music session.
  - Alternate command: `.sh`
- **Pop Command**: Use `.pop {n}` to remove a specific track from the queue based on its position. If no position is specified, the last track in the queue is removed.
  - Alternate command: `.pp`


## Getting Started
With the discontinuation of several popular Discord music bots, MusicBot serves as a self-hosted alternative, giving you the freedom to run it on your own server. This setup guide ensures you can have a fully functional music-playing bot, capable of streaming from YouTube and Spotify, up and running swiftly.

### Prerequisites
Before beginning, ensure you have a suitable hosting solution for the bot, such as a Raspberry Pi, a cloud server, or a dedicated home server. A static IP address is not required.

### Step 1: Creating Your Bot
1. Visit the [Discord Developer Portal](https://discord.com/developers/applications).
2. Log in and click "New Application" in the top right corner.
3. Name your application (e.g., "MusicBot").
4. Optionally, customize your bot's profile (name, picture, etc.) post-creation.
5. Navigate to the "Bot" tab, assign a username for your bot, and enable the "Message Content Intent" to facilitate command processing.

### Step 2: Adding Your Bot to a Server
1. Within the Developer Portal, proceed to the "OAuth2" section.
2. Under "URL generator", choose "bot" and then select "Administrator" under "Bot Permissions" for comprehensive functionality (alternatively, opt for more restrictive permissions as needed).
3. Copy the generated URL, open it in your browser, select your server, and authorize the bot.

### Step 3: Activating Your Bot
1. Download the MusicBot code from this repository.
2. Ensure Python 3.8 or newer is installed on your host machine.
3. Install the necessary dependencies by executing `pip install -r requirements.txt` in your terminal.
4. Copy the ".env_example" file, renaming the duplicate to ".env".
5. Retrieve your bot's token from the Bot section on the Developer Portal and input it into your ".env" file.
6. Start the bot with `python musicbot.py`, making the script executable on Linux/Unix systems (`chmod +x musicbot.py`).

Your MusicBot is now ready to liven up your Discord server! Test its functionality by joining a VC and experimenting with the commands. Should you encounter any issues or have queries, don't hesitate to seek support.
