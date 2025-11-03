const {
    getVoiceConnection,
    joinVoiceChannel,
    createAudioPlayer,
    createAudioResource,
    AudioPlayerStatus,
    VoiceConnectionStatus,
    entersState
} = require('@discordjs/voice');
const { EmbedBuilder } = require('discord.js');
const { saveChannel, removeChannel } = require('../utils/database');

const mp3_link = "https://hitradio-maroc.ice.infomaniak.ch/hitradio-maroc-128.mp3";

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
    }

    sendEmbed(color, description, emoji = '') {
        const embed = new EmbedBuilder()
            .setColor(color)
            .setDescription(`${emoji} ${description}`);
        this.interaction.reply({ embeds: [embed], ephemeral: true });
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
        this.connection.on('stateChange', (oldState, newState) => {
            console.log(`Connection state changed: ${oldState.status} -> ${newState.status}`);
            if (newState.status === VoiceConnectionStatus.Disconnected) {
                console.log('Voice connection disconnected');
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
                const resource = createHitRadioResource();
                player.play(resource);
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

module.exports = { Player, mp3_link };