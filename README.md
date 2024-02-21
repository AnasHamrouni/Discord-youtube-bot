### BASED ON https://github.com/maxcutlyp/YoutubeBot, MANY THANKS <3
# YoutubeBot: Your Personal Discord Bot for YouTube Playback

Welcome to the YoutubeBot repository! This Discord bot is designed to enhance your server with the ability to play YouTube videos directly in your voice channels. It's a perfect solution for shared music experiences or just adding a bit of fun to your server's voice chats. Let's dive into how you can get this bot up and running for your community.

## Features
- **Play Command**: Use `.play {url or search term}` to play a specific video or search for one. If the bot isn't already in a voice channel (VC), it will join one.
  - Alternate command: `.p`
- **Skip Command**: Use `.skip {n}` to skip a specified number of videos in the queue. If no number is provided, it skips the current video. Use `.skip all` to clear the queue and leave the VC.
  - Alternate command: `.s`
- **Queue Command**: Use `.queue` to display the current list of videos queued for playback.
  - Alternate command: `.q`
- **Shuffle Command**: Use `.shuffle` to randomly shuffle the order of videos in the queue, adding an element of surprise to your playback.
  - Alternate command: `.sh`
- **Pop Command**: Use `.pop {n}` to remove a specific video from the queue based on its position. If no position is specified, the last video in the queue will be removed.
  - Alternate command: `.pp`
## Getting Started

In light of recent events where popular Discord music bots have been discontinued, YoutubeBot offers a self-hosted alternative that you can run on your own server. This guide will help you through the setup process, ensuring you have your own YouTube-playing bot in no time.

### Prerequisites

Before we start, please ensure you have a hosting solution for the bot, such as a Raspberry Pi, an AWS server, or a home server. A static IP is not necessary for this setup.

### Step 1: Creating Your Bot

1. Navigate to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Sign in and click on "New Application" in the top right.
3. Name your application (e.g., "YoutubeBot").
4. After creation, you can customize your bot's profile (name, picture, etc.) if desired.
5. Go to the "Bot" tab, set a username for your bot, and enable the "Message Content Intent" to allow command reading.

### Step 2: Adding Your Bot to a Server

1. In the Developer Portal, go to the "OAuth2" section.
2. Under "URL generator", select "bot", then choose "Administrator" under "Bot Permissions" for full functionality (or more restrictive permissions if you prefer).
3. Copy the generated URL, paste it into your browser, select your server, and authorize the bot.

### Step 3: Activating Your Bot

1. Download the bot code from this repository.
2. Ensure Python 3.8 or later is installed on your machine.
3. Install the required dependencies by running `pip install -r requirements.txt` in your terminal.
4. Duplicate the ".env_example" file and rename the copy to ".env".
5. Obtain your bot's token from the Bot page on the Developer Portal and paste it into your ".env" file.
6. Launch the bot using `nohup ./youtubebot.py &` on Linux/Unix or `python youtubebot.py` on Windows. Ensure the script is executable if you're on Linux/Unix.

Congratulations! Your YoutubeBot should now be operational. Test it by joining a VC and using the commands. If you encounter any issues or have questions, feel free to reach out for support.
