const { ActivityType } = require('discord.js');
const config = require('../config.json');
const { loadCommands } = require("../loaders/commandLoader");
const { getAllChannels, removeChannel } = require('../utils/database');
const {
    joinVoiceChannel,
    createAudioPlayer,
    AudioPlayerStatus,
    VoiceConnectionStatus,
} = require('@discordjs/voice');
const { createHitRadioResource, waitForReady } = require('../utils/player');

module.exports = {
    name: 'ready',
    once: true,
    async execute(client) {
        console.log(`Logged in as ${client.user.tag}!`);

        loadCommands(client);

        const savedChannels = getAllChannels();
        const STAGGER_MS = 4000;
        const INITIAL_DELAY_MS = 15000;

        setTimeout(() => {
            let delayMs = 0;
            savedChannels.forEach(({ guildId, channelId }) => {
                setTimeout(async () => {
                    try {
                        const guild = await client.guilds.fetch(guildId);
                        const channel = await guild.channels.fetch(channelId);

                        if (!channel || !channel.isVoiceBased()) {
                            removeChannel(guildId);
                            return;
                        }

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
                                } catch (err) {}
                            }
                        });

                        waitForReady(connection, 60e3)
                            .then(() => {
                                if (connectionDestroyed) return;

                                const player = createAudioPlayer();

                                player.on(AudioPlayerStatus.Idle, () => {
                                    setTimeout(() => {
                                        try {
                                            player.play(createHitRadioResource());
                                        } catch (err) {
                                            console.error(`Failed to restart stream in guild ${guildId}:`, err.message);
                                        }
                                    }, 3000);
                                });

                                player.on('error', error => {
                                    console.error(`AudioPlayer Error in guild ${guildId}:`, error.message);
                                    setTimeout(() => {
                                        try {
                                            player.play(createHitRadioResource());
                                        } catch (err) {
                                            console.error(`Failed to recover in guild ${guildId}:`, err.message);
                                        }
                                    }, 3000);
                                });

                                player.play(createHitRadioResource());
                                connection.subscribe(player);
                                console.log(`Started playing in guild ${guildId}, channel ${channelId}`);
                            })
                            .catch(error => {
                                console.error(`Failed to connect to voice in guild ${guildId}:`, error.message);
                                if (!connectionDestroyed) {
                                    connectionDestroyed = true;
                                    try {
                                        connection.destroy();
                                    } catch (err) {}
                                }
                            });
                    } catch (error) {
                        if (error.code === 10004 || error.code === 10003) {
                            removeChannel(guildId);
                        }
                        console.error(`Failed to rejoin channel ${channelId} in guild ${guildId}:`, error.message);
                    }
                }, delayMs);
                delayMs += STAGGER_MS;
            });
        }, INITIAL_DELAY_MS);

        let index = 0;
        const statusMessages = config.statusMessages;
        const intervalMs = (config.statusInterval || 30) * 1000;

        setInterval(() => {
            if (index >= statusMessages.length) index = 0;
            client.user.setActivity(statusMessages[index], { type: ActivityType.Listening });
            index++;
        }, intervalMs);
    },
};
