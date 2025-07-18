const { ActivityType } = require('discord.js');
const config = require('../config.json');
const { loadCommands } = require("../loaders/commandLoader");
const { getAllChannels } = require('../utils/database');
const {
    joinVoiceChannel,
    createAudioPlayer,
    createAudioResource,
    AudioPlayerStatus
} = require('@discordjs/voice');
const { mp3_link } = require('../utils/player');

function createHitRadioResource() {
    return createAudioResource(mp3_link);
}

module.exports = {
    name: 'ready',
    once: true,
    async execute(client) {
        console.log(`Logged in as ${client.user.tag}!`);

        loadCommands(client);

        const savedChannels = getAllChannels();
        for (const { guildId, channelId } of savedChannels) {
            try {
                const guild = await client.guilds.fetch(guildId);
                const channel = await guild.channels.fetch(channelId);

                if (channel && channel.isVoiceBased()) {
                    const connection = joinVoiceChannel({
                        channelId: channel.id,
                        guildId: channel.guild.id,
                        adapterCreator: channel.guild.voiceAdapterCreator,
                    });

                    const player = createAudioPlayer();
                    player.play(createHitRadioResource());
                    connection.subscribe(player);

                    player.on(AudioPlayerStatus.Idle, () => {
                        player.play(createHitRadioResource());
                    });

                    player.on('error', error => {
                        console.error(`Error in guild ${guildId}, channel ${channelId}:`, error.message);
                        player.play(createHitRadioResource());
                    });

                    } else {
                    // Skipping auto-join for guild ${guildId}, channel ${channelId}: Channel not found or not a voice channel.
                    // console.log(`Skipping auto-join for guild ${guildId}, channel ${channelId}: Channel not found or not a voice channel.`);
                }
            } catch (error) {
                console.error(`Failed to rejoin channel ${channelId} in guild ${guildId}:`, error.message);
            }
        }

        let index = 0;
        const statusMessages = config.statusMessages;
        const intervalSeconds = config.statusInterval * 1000;

        setInterval(() => {
            if (index >= statusMessages.length) {
                index = 0; // Reset to the first message if we've gone through all of them
            }
            client.user.setActivity(statusMessages[index], { type: ActivityType.Listening });
            index++;
        }, intervalSeconds);
    },
};
