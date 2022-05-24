import discord
import shared.lavalinkclass as lavalinkclass

from private.essentials import LAVA_HOST, LAVA_PORT, LAVA_PASSWORD, LAVA_REGION, LAVA_NAME

class LavalinkVoiceClient(discord.VoiceClient):

    def __init__(self, client: discord.Client, channel: discord.abc.Connectable):
        self.client = client
        self.channel = channel
        
        if hasattr(self.client, 'lavalink'):
            self.lavalink = self.client.lavalink
        else:
            self.client.lavalink = lavalinkclass.Client(client.user.id)
            self.client.lavalink.add_node(
                    LAVA_HOST,
                    LAVA_PORT,
                    LAVA_PASSWORD,
                    LAVA_REGION,
                    LAVA_NAME)
            self.lavalink = self.client.lavalink

    async def on_voice_server_update(self, data):
        
        lavalink_data = {
                't': 'VOICE_SERVER_UPDATE',
                'd': data
                }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def on_voice_state_update(self, data):
        
        lavalink_data = {
                't': 'VOICE_STATE_UPDATE',
                'd': data
                }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def connect(self, *, timeout: float, reconnect: bool = True, self_deaf: bool = True) -> None:
        
        self.lavalink.player_manager.create(guild_id = self.channel.guild.id)
        await self.channel.guild.change_voice_state(channel = self.channel, self_deaf = self_deaf)

    async def disconnect(self, *, force: bool) -> None:
        
        player = self.lavalink.player_manager.get(self.channel.guild.id)
        
        if not force and not player.is_connected:
            return
            
        await self.channel.guild.change_voice_state(channel=None)
        
        player.channel_id = None
        self.cleanup()