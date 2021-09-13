import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

client = commands.Bot(command_prefix='.')
players = {}
@client.event
async def on_ready():
    print('MUSIC BOT STARTED')
@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
@client.command()
async def play(ctx, *url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected:
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
    URL = info['url']
    voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    voice.is_playing()
    await ctx.send('Bot is playing')
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('Bot is resuming')
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Bot has been paused')
@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice:
        voice.stop()
        await ctx.send('Stopping...')
@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Messages have been cleared")
client.run('ODA0MzU0Nzc5NDUwNzAzOTEz.YBLHww.Wr4rCTuDupH-GIRTKpH4AZ205Ms')
