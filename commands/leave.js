const { SlashCommandBuilder } = require('discord.js');
const { Player } = require('../utils/player');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('leave')
        .setDescription('👋 Leave the voice channel.'),
    async execute(interaction) {
        const player = new Player(interaction);
        player.leaveChannel();
    },
};
