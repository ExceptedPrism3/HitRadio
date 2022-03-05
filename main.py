from re import T
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

# Import the Bot-Token


intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = 'hr!', intents = intents)


@client.event
async def on_ready():
    print("The bot has Started!")
    print("--------------------")


@client.command()
async def helpo(ctx):
    await ctx.send("/play")
    await ctx.send("/leave")
    await ctx.send("/vote")
    await ctx.send("/invite")

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('')
        await ctx.send("I have joined the channel")
    else:
        await ctx.send("You must be in a voice channel to run this command.")

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I have left the voice channel.")
    else:
        await ctx.send("I'm not in a voice channel.")


client.run('')


# import os

# from discord import FFmpegPCMAudio
# from discord.ext.commands import Bot
# from dotenv import load_dotenv

# load_dotenv()
# TOKEN = os.getenv('OTQ5NjI5MzIwMTEwOTQ0MjU2.YiNJOQ.U1JeAWyHZtvWBJzv2kWY5pg9ryE')
# PREFIX = os.getenv('!')

# client = Bot(command_prefix=list(PREFIX))


# @client.event
# async def on_ready():
#     print('Music Bot Ready')


# @client.command(aliases=['p', 'pla'])
# async def play(ctx, url: str = 'http://stream.radioparadise.com/rock-128'):
#     channel = ctx.message.author.voice.channel
#     global player
#     try:
#         player = await channel.connect()
#     except:
#         pass
#     player.play(FFmpegPCMAudio('http://stream.radioparadise.com/rock-128'))


# @client.command(aliases=['s', 'sto'])
# async def stop(ctx):
#     player.stop()


# client.run(TOKEN)

# from pydoc import cli
# import discord
# from discord.ext import commands


# client = commands.Bot(command_prefix = '!')

# @client.event
# async def on_ready():
#     print("The bot has Started!")


# @client.command()
# async def play(ctx, url_ : str):

#     voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = '🚨Staff-Side🚨')
#     voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
#     if not voice.is_connected():
#         await voiceChannel.connect()


# client.run('OTQ5NjI5MzIwMTEwOTQ0MjU2.YiNJOQ.U1JeAWyHZtvWBJzv2kWY5pg9ryE')