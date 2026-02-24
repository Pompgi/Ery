import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import yt_dlp
import asyncio
import random
from triggers import check_triggers

# Load token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Custom prefix
PREFIX = "Ery "  # change this to whatever you want

# Bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# FFmpeg options
ffmpeg_options = {
    "options": "-vn"
}

# First join flag
first_join = True

# On ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


# Automatic response for "stuff"
@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    content = message.content.lower()
    
    # Check triggers using the separate module
    should_return = await check_triggers(message, content)
    if should_return:
        return

    # Always process commands last
    await bot.process_commands(message)

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if not ctx.voice_client:
            await channel.connect()

        # Always Rick Roll when summoned
        rick_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        await play_song(ctx, rick_url, rickroll=True)
    else:
        await ctx.send("Go into a voice channel bruh...")

# Leave command
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

# Play command
@bot.command()
async def play(ctx, *, query: str):
    if not ctx.author.voice:
        await ctx.send("Go into a voice channel bruh...")
        return
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()

    # Use ytsearch1 if not a URL
    if not query.startswith("http"):
        query = f"ytsearch1:{query}"

    await play_song(ctx, query)


# Helper function to download and play a song
async def play_song(ctx, query, rickroll=False):
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "outtmpl": "temp_audio.%(ext)s"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        if "entries" in info:  # search results
            info = info["entries"][0]
        filename = ydl.prepare_filename(info)
        title = info.get("title", "Unknown Song")

    source = discord.FFmpegOpusAudio(
        executable="C:/ffmpeg/bin/ffmpeg.exe",  # <-- your FFmpeg path
        source=filename,
        **ffmpeg_options
    )

    # Stop any currently playing audio
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    ctx.voice_client.play(source)
    # Message
    if rickroll:
        await ctx.send("Bish! You just got Rick Rolled! *starts breakdancing* 🎵")
        await asyncio.sleep(5)  # wait 5 seconds
        await ctx.send("*falls down* augh my back")
    else:
        await ctx.send(f"Now playing: {title} 🎧")

    # Wait until finished, then delete temp file
    while ctx.voice_client.is_playing():
        await asyncio.sleep(1)

    try:
        os.remove(filename)
    except Exception as e:
        print(f"Failed to delete temp file: {e}")


# Run the bot
bot.run(TOKEN)
