const {
    getVoiceConnection,
    joinVoiceChannel,
    createAudioPlayer,
    createAudioResource,
    AudioPlayerStatus,
    VoiceConnectionStatus,
    entersState,
    StreamType,
} = require('@discordjs/voice');
const { EmbedBuilder, ActionRowBuilder, ButtonBuilder, ButtonStyle } = require('discord.js');
const { saveChannel, removeChannel } = require('../utils/database');
const config = require('../config.json');

const mp3_link = config.radioUrl;

function waitForReady(connection, timeoutMs = 60e3) {
    return new Promise((resolve, reject) => {
        if (connection.state.status === VoiceConnectionStatus.Ready) {
            resolve();
            return;
        }
        const timeout = setTimeout(() => {
            connection.removeListener(VoiceConnectionStatus.Ready, onReady);
            connection.removeListener(VoiceConnectionStatus.Destroyed, onDestroyed);
            reject(new Error('Voice connection timed out'));
        }, timeoutMs);
        const onReady = () => {
            clearTimeout(timeout);
            connection.removeListener(VoiceConnectionStatus.Destroyed, onDestroyed);
            resolve();
        };
        const onDestroyed = () => {
            clearTimeout(timeout);
            connection.removeListener(VoiceConnectionStatus.Ready, onReady);
            reject(new Error('Connection destroyed before ready'));
        };
        connection.once(VoiceConnectionStatus.Ready, onReady);
        connection.once(VoiceConnectionStatus.Destroyed, onDestroyed);
    });
}

function createHitRadioResource() {
    return createAudioResource(mp3_link, {
        inputType: StreamType.Arbitrary,
        inlineVolume: false
    });
}

/**
 * Discord voice can drop (522/521, gateway moves) while @discordjs/voice still
 * holds a VoiceConnection — then /play says "already playing" with no bot in VC.
 * If the gateway says we are not in a channel (or we're in a different one),
 * destroy the stale connection so commands work again.
 */
function pruneStaleVoiceConnection(guild) {
    const connection = getVoiceConnection(guild.id);
    if (!connection || connection.state.status === VoiceConnectionStatus.Destroyed) {
        return;
    }

    const botVoiceChannelId = guild.members.me?.voice?.channelId ?? null;

    if (botVoiceChannelId === null) {
        try {
            connection.destroy();
        } catch (_) {
            /* noop */
        }
        return;
    }

    if (connection.joinConfig.channelId !== botVoiceChannelId) {
        try {
            connection.destroy();
        } catch (_) {
            /* noop */
        }
    }
}

class Player {
    constructor(interaction) {
        this.interaction = interaction;
        pruneStaleVoiceConnection(interaction.guild);
        this.connection = getVoiceConnection(interaction.guild.id);
        if (this.connection) {
            this.connection.rejoinAttempts = 0;
        }
    }

    sendEmbed(color, description, emoji = '') {
        const embed = new EmbedBuilder()
            .setColor(color)
            .setDescription(`${emoji} ${description}`);

        const components = [];

        if (color === '#00FF00' && description.includes('Now playing')) {
            const stopButton = new ButtonBuilder()
                .setCustomId('stop_radio')
                .setLabel('Stop Radio')
                .setStyle(ButtonStyle.Danger)
                .setEmoji('🛑');

            const row = new ActionRowBuilder().addComponents(stopButton);
            components.push(row);
        }

        const payload = { embeds: [embed], components };
        if (this.interaction.deferred) {
            return this.interaction.editReply(payload);
        }
        return this.interaction.reply({ ...payload, ephemeral: true });
    }

    checkUserInVoiceChannel() {
        const userChannel = this.interaction.member.voice.channel;
        if (!userChannel) {
            this.sendEmbed('#FF0000', 'You need to join a voice channel first!', '❌');
            return null;
        }
        return userChannel;
    }

    checkBotInVoiceChannel(userChannel) {
        if (this.connection) {
            const botChannel = this.connection.joinConfig.channelId;
            if (botChannel === userChannel.id) {
                this.sendEmbed('#FFFF00', 'I am already playing music in this voice channel!', '⚠️');
                return true;
            } else {
                this.sendEmbed('#FF0000', 'I am already playing music in another voice channel!', '❌');
                return true;
            }
        }
        return false;
    }

    async playMusic() {
        const userChannel = this.checkUserInVoiceChannel();
        if (!userChannel) return;

        if (this.checkBotInVoiceChannel(userChannel)) return;

        await this.interaction.deferReply({ ephemeral: true });

        console.log(`Attempting to join voice channel ${userChannel.id} in guild ${userChannel.guild.id}`);

        this.connection = joinVoiceChannel({
            channelId: userChannel.id,
            guildId: userChannel.guild.id,
            adapterCreator: userChannel.guild.voiceAdapterCreator,
        });

        this.connection.on('stateChange', async (oldState, newState) => {
            console.log(`Connection state changed: ${oldState.status} -> ${newState.status}`);

            if (newState.status === VoiceConnectionStatus.Disconnected) {
                if (newState.reason === 4014 && newState.closeCode === 4014) {
                    try {
                        await entersState(this.connection, VoiceConnectionStatus.Connecting, 20_000);
                    } catch {
                        if (this.connection.state.status !== VoiceConnectionStatus.Destroyed) {
                            this.connection.destroy();
                        }
                    }
                } else if (this.connection.rejoinAttempts < 15) {
                    await new Promise(resolve => setTimeout(resolve, (this.connection.rejoinAttempts + 1) * 2000));
                    this.connection.rejoin();
                    this.connection.rejoinAttempts++;
                } else {
                    if (this.connection.state.status !== VoiceConnectionStatus.Destroyed) {
                        this.connection.destroy();
                    }
                }
            } else if (newState.status === VoiceConnectionStatus.Destroyed) {
                console.log('Voice connection destroyed.');
            } else if (newState.status === VoiceConnectionStatus.Connecting || newState.status === VoiceConnectionStatus.Signalling) {
                this.connection.rejoinAttempts = 0;
            }
        });

        this.connection.on('error', error => {
            console.error('VoiceConnection Error:', error.message);
        });

        saveChannel(userChannel.guild.id, userChannel.id);

        try {
            console.log('Waiting for connection to be ready...');
            await waitForReady(this.connection, 60e3);
            console.log('Connection is ready, starting audio player...');

            const player = createAudioPlayer();

            player.on(AudioPlayerStatus.Idle, () => {
                setTimeout(() => {
                    try {
                        const resource = createHitRadioResource();
                        player.play(resource);
                    } catch (error) {
                        console.error('Failed to restart stream:', error);
                    }
                }, 3000);
            });

            player.on('error', error => {
                console.error('AudioPlayer Error:', error.message);
                setTimeout(() => {
                    try {
                        const resource = createHitRadioResource();
                        player.play(resource);
                    } catch (err) {
                        console.error('Failed to recover from error:', err.message);
                    }
                }, 3000);
            });

            const resource = createHitRadioResource();
            player.play(resource);
            this.connection.subscribe(player);
            console.log('Audio player started and subscribed to connection');

            this.sendEmbed('#00FF00', 'Now playing the Hits 24/7!', '🎶');
        } catch (error) {
            console.error('Failed to play audio:', error.message);
            if (this.connection) {
                this.connection.destroy();
            }
            this.sendEmbed('#FF0000', `Failed to connect to voice channel: ${error.message}`, '❌');
        }
    }

    leaveChannel() {
        const userChannel = this.checkUserInVoiceChannel();
        if (!userChannel) return;

        if (!this.connection) {
            this.sendEmbed('#FF0000', 'I am not in any voice channel!', '❌');
            return;
        }

        const botChannel = this.connection.joinConfig.channelId;
        if (botChannel !== userChannel.id) {
            this.sendEmbed('#FF0000', 'You need to be in the same voice channel as me to use this command!', '❌');
            return;
        }

        this.connection.destroy();
        removeChannel(userChannel.guild.id);
        this.sendEmbed('#00FF00', 'Left the voice channel!', '👋');
    }
}

module.exports = { Player, mp3_link, createHitRadioResource, waitForReady };
