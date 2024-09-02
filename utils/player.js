const {
    getVoiceConnection,
    joinVoiceChannel,
    createAudioPlayer,
    createAudioResource,
    AudioPlayerStatus
} = require('@discordjs/voice');
const { EmbedBuilder } = require('discord.js');

function sendEmbed(interaction, color, description, emoji = '') {
    const embed = new EmbedBuilder()
        .setColor(color)
        .setDescription(`${emoji} ${description}`);
    interaction.reply({ embeds: [embed], ephemeral: true });
}

function checkUserInVoiceChannel(interaction) {
    const userChannel = interaction.member.voice.channel;
    if (!userChannel) {
        sendEmbed(interaction, '#FF0000', 'You need to join a voice channel first!', '❌');
        return null;
    }
    return userChannel;
}

function checkBotInVoiceChannel(interaction, userChannel) {
    const connection = getVoiceConnection(interaction.guild.id);
    if (connection) {
        const botChannel = connection.joinConfig.channelId;
        if (botChannel === userChannel.id) {
            sendEmbed(interaction, '#FFFF00', 'I am already playing music in this voice channel!', '⚠️');
            return true;
        } else {
            sendEmbed(interaction, '#FF0000', 'I am already playing music in another voice channel!', '❌');
            return true;
        }
    }
    return false;
}

function playMusic(interaction) {
    const userChannel = checkUserInVoiceChannel(interaction);
    if (!userChannel) return;

    if (checkBotInVoiceChannel(interaction, userChannel)) return;

    const connection = joinVoiceChannel({
        channelId: userChannel.id,
        guildId: userChannel.guild.id,
        adapterCreator: userChannel.guild.voiceAdapterCreator,
    });

    const player = createAudioPlayer();
    const mp3_link = "https://hitradio-maroc.ice.infomaniak.ch/hitradio-maroc-128.mp3";
    const resource = createAudioResource(mp3_link);

    player.play(resource);
    connection.subscribe(player);

    // Continuous 24/7 playback
    player.on(AudioPlayerStatus.Idle, () => {
        const newResource = createAudioResource(mp3_link);
        player.play(newResource);
    });

    player.on('error', error => {
        console.error('Error:', error.message);
        const newResource = createAudioResource(mp3_link);
        player.play(newResource);
    });

    sendEmbed(interaction, '#00FF00', 'Now playing the Hits 24/7!', '🎶');
}

function leaveChannel(interaction) {
    const userChannel = checkUserInVoiceChannel(interaction);
    if (!userChannel) return;

    const connection = getVoiceConnection(interaction.guild.id);
    if (!connection) {
        sendEmbed(interaction, '#FF0000', 'I am not in any voice channel!', '❌');
        return;
    }

    const botChannel = connection.joinConfig.channelId;
    if (botChannel !== userChannel.id) {
        sendEmbed(interaction, '#FF0000', 'You need to be in the same voice channel as me to use this command!', '❌');
        return;
    }

    connection.destroy();
    sendEmbed(interaction, '#00FF00', 'Left the voice channel!', '👋');
}

module.exports = { playMusic, leaveChannel };
