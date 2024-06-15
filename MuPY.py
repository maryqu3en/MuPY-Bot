import discord
from discord.ext import commands
from dotenv import load_dotenv
import yt_dlp
import asyncio
import re
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

FFMPEG_OPTIONS = {'options' : '-vn'}
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist' : False}


class MuPY(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []
        self.current_playlist = []

    @commands.command()
    async def play(self, ctx, *, search):
        if ctx.voice_client is None:
            if ctx.author.voice is None:
                await ctx.send("You are not in a voice channel!")
                return
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect()

        async with ctx.typing():
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                url_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+'
                if re.match(url_regex, search):
                    info = ydl.extract_info(search, download=False)
                    if 'entries' in info:
                        # It's a playlist
                        self.current_playlist = info['entries']
                        video = self.current_playlist.pop(0)
                        url = video['url']
                        title = video['title']
                        self.queue.append((url, title))
                        await ctx.send(f'Added to queue: **{title}** from playlist: **{info["title"]}**')
                    else:
                        # It's a single video
                        url = info['url']
                        title = info['title']
                        self.queue.append((url, title))
                        await ctx.send(f'Added to queue: **{title}**')
                else:
                    info = ydl.extract_info(f"ytsearch:{search}", download=False)
                    if 'entries' in info:
                        if not info['entries']:
                            await ctx.send("No results found!")
                            return
                        info = info['entries'][0]
                    url = info['url']
                    title = info['title']
                    self.queue.append((url, title))
                    await ctx.send(f'Added to queue: **{title}**')

            if not ctx.voice_client.is_playing():
                await self.play_next(ctx)

    async def play_next(self, ctx):
        if ctx.voice_client and self.queue:
            url, title = self.queue.pop(0)
            print(f"URL: {url}, Title: {title}")
            try:
                source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
            except Exception as e:
                print(f"Error creating audio source: {e}")
                return
            try:
                ctx.voice_client.play(source, after=lambda e: self.client.loop.create_task(self.check_queue(ctx)))
            except Exception as e:
                print(f"Error playing audio: {e}")
                return
            await ctx.send(f'Now playing: **{title}**')

    async def check_queue(self, ctx):
        if self.current_playlist:
            video = self.current_playlist.pop(0)
            url = video['url']
            title = video['title']
            self.queue.append((url, title))
            await self.play_next(ctx)
        elif self.queue:
            await self.play_next(ctx)
        else:
            await ctx.send("Queue is empty!")
            await asyncio.sleep(180)
            if ctx.voice_client:
                await ctx.voice_client.disconnect()



    # --------------------------------------------------------------- #
    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipped!")
            await self.play_next(ctx)
        else:
            await ctx.send("Nothing is playing!")

    # --------------------------------------------------------------- #
    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("Left voice channel!")

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("Paused!")

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("Resumed!")

    @commands.command()
    async def stop(self, ctx):
        ctx.voice_client.stop()
        await ctx.send("Stopped!")
    # --------------------------------------------------------------- #

def get_prefix(bot, message):
    prefixes = ['mu!', 'Mu!']

    for prefix in prefixes:
        if message.content.startswith(prefix):
            return prefix

    return commands.when_mentioned(bot, message)

client = commands.Bot(command_prefix=get_prefix, intents=intents)
async def main():
    await client.add_cog(MuPY(client))
    await client.start(os.getenv('BOTTOKEN'))
asyncio.run(main())