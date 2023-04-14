import discord
import shared.lavalinkclass as lavalinkclass

from private.essentials import LAVA_HOST, LAVA_PORT, LAVA_PASSWORD, LAVA_REGION, LAVA_NAME


class LavalinkVoiceClient(discord.VoiceClient):

    def __init__(self, client: discord.Client, channel: discord.abc.Connectable):
        super().__init__(client, channel)
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

    async def connect(self, *, timeout: float, reconnect: bool = True, self_deaf: bool = True) -> None:
        """
        Connect to the voice channel and create a player for the guild
        """
        self.lavalink.player_manager.create(guild_id=self.channel.guild.id)
        voice_client = await self.channel.connect(cls=LavalinkVoiceClient)
        voice_client.self_deaf = self_deaf

    async def disconnect(self, *, force: bool) -> None:
        """
        Disconnect from the voice channel and cleanup the player
        """
        player = self.lavalink.player_manager.get(self.channel.guild.id)

        if not force and not player.is_connected:
            return

        await self.channel.guild.voice_client.disconnect()
        player.channel_id = None
        self.cleanup()

    async def on_voice_update(self, data: dict) -> None:
        """
        Handler for both on_voice_server_update and on_voice_state_update events
        """
        lavalink_data = {
            't': data.get('t'),
            'd': {
                'guild_id': data['d']['guild_id'],
                'session_id': data['d']['session_id'],
                'event': data['d']
            }
        }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def on_voice_server_update(self, data: dict) -> None:
        """
        Event handler for when the voice server updates
        """
        await self.on_voice_update(data)

    async def on_voice_state_update(self, data: dict) -> None:
        """
        Event handler for when the voice state updates
        """
        await self.on_voice_update(data)
