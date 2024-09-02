const { SlashCommandBuilder } = require('discord.js');
const { playMusic } = require('../utils/player');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('play')
        .setDescription('🎶 Play Hits in your voice channel.'),
    async execute(interaction) {
        playMusic(interaction);
    },
};
