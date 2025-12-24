const {
    getVoiceConnection,
    joinVoiceChannel,
    createAudioPlayer,
    createAudioResource,
    AudioPlayerStatus,
    VoiceConnectionStatus,
    entersState
} = require('@discordjs/voice');
const { EmbedBuilder, ActionRowBuilder, ButtonBuilder, ButtonStyle } = require('discord.js');
const { saveChannel, removeChannel } = require('../utils/database');
const config = require('../config.json');

const mp3_link = config.radioUrl;

function createHitRadioResource() {
    return createAudioResource(mp3_link, {
        inputType: 'unknown',
        inlineVolume: false
    });
}

class Player {
    constructor(interaction) {
        this.interaction = interaction;
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

        this.interaction.reply({ embeds: [embed], components: components, ephemeral: true });
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

        console.log(`Attempting to join voice channel ${userChannel.id} in guild ${userChannel.guild.id}`);

        this.connection = joinVoiceChannel({
            channelId: userChannel.id,
            guildId: userChannel.guild.id,
            adapterCreator: userChannel.guild.voiceAdapterCreator,
        });

        // Track connection state changes
        // Track connection state changes
        this.connection.on('stateChange', async (oldState, newState) => {
            console.log(`Connection state changed: ${oldState.status} -> ${newState.status}`);

            if (newState.status === VoiceConnectionStatus.Disconnected) {
                if (newState.reason === 4014 && newState.closeCode === 4014) {
                    // Don't manually destroy, Discord handles this for channel moves
                    // Wait for Reconnecting state
                    try {
                        await entersState(this.connection, VoiceConnectionStatus.Connecting, 20_000);
                        // Probably moved voice channel
                    } catch {
                        // Failed to reconnect, might have been kicked
                        if (this.connection.state.status !== VoiceConnectionStatus.Destroyed) {
                            this.connection.destroy();
                        }
                    }
                } else if (this.connection.rejoinAttempts < 5) {
                    // unexpected disconnect, wait and try to reconnect
                    await new Promise(resolve => setTimeout(resolve, (this.connection.rejoinAttempts + 1) * 1000));
                    this.connection.rejoin();
                    this.connection.rejoinAttempts++;
                } else {
                    if (this.connection.state.status !== VoiceConnectionStatus.Destroyed) {
                        this.connection.destroy();
                    }
                }
            } else if (newState.status === VoiceConnectionStatus.Destroyed) {
                // If destroyed unexpectedly (not by /stop), try to restart cycle
                // Note: user.leaveChannel() calls destroy() manually, so we need to know if it was manual.
                // For now, rely on persisted DB + pm2 restart if needed, or simple rejoin logic if we can detect it.
                // Since we removed removeChannel from ready.js error handler, 
                // simply letting it die allows the persistence to work on next ready() trigger or restart.
                console.log('Voice connection destroyed.');
            } else if (newState.status === VoiceConnectionStatus.Connecting || newState.status === VoiceConnectionStatus.Signalling) {
                this.connection.rejoinAttempts = 0;
            }
        });

        // Only destroy on critical errors, not all errors
        this.connection.on('error', error => {
            console.error('VoiceConnection Error:', error.message);
            // Don't auto-destroy on error, let it try to recover
        });

        saveChannel(userChannel.guild.id, userChannel.id);

        try {
            console.log('Waiting for connection to be ready...');
            // Wait for the connection to be ready before playing audio
            await entersState(this.connection, VoiceConnectionStatus.Ready, 30e3);
            console.log('Connection is ready, starting audio player...');

            const player = createAudioPlayer();

            player.on(AudioPlayerStatus.Idle, () => {
                // Wait a bit before trying to play again to avoid spamming if the stream is dead
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
                // Try to recover by playing a new resource
                try {
                    const resource = createHitRadioResource();
                    player.play(resource);
                } catch (err) {
                    console.error('Failed to recover from error:', err.message);
                }
            });

            // Start playing
            const resource = createHitRadioResource();
            player.play(resource);
            this.connection.subscribe(player);
            console.log('Audio player started and subscribed to connection');

            this.sendEmbed('#00FF00', 'Now playing the Hits 24/7!', '🎶');
        } catch (error) {
            console.error('Failed to play audio:', error.message);
            console.error('Error details:', error);
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

module.exports = { Player, mp3_link, createHitRadioResource };