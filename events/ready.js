const { ActivityType } = require('discord.js');
const config = require('../config.json');
const { loadCommands } = require("../loaders/commandLoader");
const { getAllChannels, removeChannel } = require('../utils/database');
const {
    joinVoiceChannel,
    createAudioPlayer,
    createAudioResource,
    AudioPlayerStatus,
    VoiceConnectionStatus,
    entersState
} = require('@discordjs/voice');
const { mp3_link } = require('../utils/player');

function createHitRadioResource() {
    return createAudioResource(mp3_link, {
        inputType: 'unknown',
        inlineVolume: false
    });
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

                    let connectionDestroyed = false;

                    connection.on('error', error => {
                        console.error(`VoiceConnection Error in guild ${guildId}:`, error.message);
                        if (!connectionDestroyed) {
                            connectionDestroyed = true;
                            try {
                                connection.destroy();
                            } catch (err) {
                                // Connection already destroyed, ignore
                            }
                            removeChannel(guildId);
                        }
                    });

                    // Wait for connection to be ready, then start playing
                    entersState(connection, VoiceConnectionStatus.Ready, 20e3)
                        .then(() => {
                            if (connectionDestroyed) return;
                            
                            const player = createAudioPlayer();
                            
                            player.on(AudioPlayerStatus.Idle, () => {
                                const resource = createHitRadioResource();
                                player.play(resource);
                            });

                            player.on('error', error => {
                                console.error(`AudioPlayer Error in guild ${guildId}, channel ${channelId}:`, error.message);
                                try {
                                    const resource = createHitRadioResource();
                                    player.play(resource);
                                } catch (err) {
                                    console.error(`Failed to recover in guild ${guildId}:`, err.message);
                                }
                            });

                            // Start playing
                            const resource = createHitRadioResource();
                            player.play(resource);
                            connection.subscribe(player);
                            console.log(`Started playing in guild ${guildId}, channel ${channelId}`);
                        })
                        .catch(error => {
                            console.error(`Failed to connect to voice in guild ${guildId}:`, error.message);
                            if (!connectionDestroyed) {
                                connectionDestroyed = true;
                                try {
                                    connection.destroy();
                                } catch (err) {
                                    // Connection already destroyed, ignore
                                }
                                removeChannel(guildId);
                            }
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
