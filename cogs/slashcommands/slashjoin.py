import discord
from discord.commands import slash_command
from shared.lavalinkclass import LavalinkVoiceClient

from private.essentials import STREAM_LINK

class Music(discord.ext.commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    async def ensure_voice(self, ctx, connect = True):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint='us')

        if player.is_connected:
            return await ctx.respond("I'm already connected to a channel.", ephemeral = True)
        
        should_connect = connect == True

        if not ctx.author.voice or not ctx.author.voice.channel:
            return await ctx.respond('You must be in a voice channel to run this command.', ephemeral = True)

        if not player.is_connected:
            if not should_connect:
                return await ctx.respond('Not connected.', ephemeral = True)

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:
                return await ctx.respond('I need the `CONNECT` and `SPEAK` permissions.', ephemeral = True)

            player.store('channel', ctx.channel.id)
            await ctx.author.voice.channel.connect(cls=LavalinkVoiceClient)

    @slash_command(description = "Joins your voice channel and play the hits.")
    async def play(self, ctx):

        await self.ensure_voice(ctx)

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
            
        results = await player.node.get_tracks(STREAM_LINK)

        player.add(requester = ctx.author.id, track = results['tracks'][0])
        
        player.store("channel", ctx.channel.id)

        player.store("guild", ctx.guild.id)

        if not player.is_playing:
            
            await player.play()
            
            return await ctx.respond(f"I have joined the {ctx.author.voice.channel.mention} channel.", ephemeral = True)

def setup(bot):

