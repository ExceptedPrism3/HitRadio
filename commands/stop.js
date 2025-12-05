const { SlashCommandBuilder } = require('discord.js');
const { Player } = require('../utils/player');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('stop')
        .setDescription('🛑 Stop the radio and leave the voice channel.'),
    async execute(interaction) {
        const player = new Player(interaction);
        player.leaveChannel();
    },
};
