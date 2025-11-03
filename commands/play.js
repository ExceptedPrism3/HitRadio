const { SlashCommandBuilder } = require('discord.js');
const { Player } = require('../utils/player');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('play')
        .setDescription('🎶 Play Hits in your voice channel.'),
    async execute(interaction) {
        const player = new Player(interaction);
        await player.playMusic();
    },
};
