class VoiceChannelUtility:
    # Static method to check the voice state of the bot in relation to the user
    @staticmethod
    async def check_voice_state(interaction, embed):
        # Get the current voice client of the guild (server)
        guild_voice_state = interaction.guild.voice_client

        # Check if the bot is not connected to any voice channel
        if not guild_voice_state or not guild_voice_state.is_connected():
            # Update the embed to show that the bot is not in any voice channel
            embed.description = "🚫 I'm not in a voice channel."
            return False  # Return False indicating the check failed

        # Check if the user is not in any voice channel or not in the same channel as the bot
        if not interaction.user.voice or interaction.user.voice.channel != guild_voice_state.channel:
            # Update the embed to show that the user is not in the same channel as the bot
            embed.description = "🚫 You need to be in the same voice channel as me to execute this command."
            return False  # Return False indicating the check failed

        # If all checks pass, return True
        return True
