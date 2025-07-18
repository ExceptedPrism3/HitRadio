const {
    getVoiceConnection,
    joinVoiceChannel,
    createAudioPlayer,
    createAudioResource,
    AudioPlayerStatus
} = require('@discordjs/voice');
const { EmbedBuilder } = require('discord.js');
const { saveChannel, removeChannel } = require('../utils/database');

const mp3_link = "https://hitradio-maroc.ice.infomaniak.ch/hitradio-maroc-128.mp3";

function createHitRadioResource() {
    return createAudioResource(mp3_link);
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

    playMusic() {
        const userChannel = this.checkUserInVoiceChannel();
        if (!userChannel) return;

        if (this.checkBotInVoiceChannel(userChannel)) return;

        this.connection = joinVoiceChannel({
            channelId: userChannel.id,
            guildId: userChannel.guild.id,
            adapterCreator: userChannel.guild.voiceAdapterCreator,
        });
        saveChannel(userChannel.guild.id, userChannel.id);

        const player = createAudioPlayer();
        player.play(createHitRadioResource());
        this.connection.subscribe(player);

        player.on(AudioPlayerStatus.Idle, () => {
            player.play(createHitRadioResource());
        });

        player.on('error', error => {
            console.error('Error:', error.message);
            player.play(createHitRadioResource());
        });

        this.sendEmbed('#00FF00', 'Now playing the Hits 24/7!', '🎶');
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