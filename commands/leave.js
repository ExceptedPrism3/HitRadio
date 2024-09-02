const { SlashCommandBuilder } = require('discord.js');
const { leaveChannel } = require('../utils/player');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('leave')
        .setDescription('👋 Leave the voice channel.'),
    async execute(interaction) {
        leaveChannel(interaction);
    },
};
