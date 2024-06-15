# MuPY - A Discord Music Bot

MuPY is a simple Discord bot written in Python using the discord.py library. It can join voice channels and play music from YouTube based on user commands.

## Features

- Join and leave voice channels
- Play music from YouTube (both single videos and playlists)
- Pause, resume, and stop music
- Skip to the next song in the queue

## Commands

- `mu!play <YouTube URL or search term>`: Adds the specified song or playlist to the queue and starts playing if not already playing.
- `mu!skip`: Skips the currently playing song and plays the next song in the queue.
- `mu!leave`: Makes the bot leave the current voice channel.
- `mu!pause`: Pauses the currently playing song.
- `mu!resume`: Resumes the paused song.
- `mu!stop`: Stops the currently playing song.

## Setup

1. Clone this repository.
2. Install the required Python packages with `pip install -r requirements.txt`.
3. Create a `.env` file in the same directory as `MuPY.py` and add your bot token like this: `BOTTOKEN=your-bot-token`.
4. Run `MuPY.py` with Python 3.7 or newer.

## Note

This bot is intended for educational purposes and may not be suitable for large-scale or commercial use.